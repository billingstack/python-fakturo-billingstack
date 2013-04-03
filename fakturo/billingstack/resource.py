import logging
import re
import simplejson as json

from fakturo.core import exceptions
from fakturo.core.provider import resource


LOG = logging.getLogger(__name__)


class Base(resource.BaseResource):
    parent = None

    resource_name = None
    resource_exclude = False

    resource_key = None

    url = None

    @classmethod
    def _item_url(cls, resource_exclude=False):
        """
        Return the url part for a single resource of this class

        :return: URL For a Item
        :rtype: string
        """
        if cls.resource_name:
            part_id = '/' + '%(' + cls.resource_name[0:-1] + '_id)s'

            return part_id if resource_exclude else '/' + \
                cls.resource_name + part_id
        else:
            return cls.url

    @classmethod
    def get_url(cls, item=False):
        """
        Get the URL for a collection / resource in this Controller

        :param item: Retrieve of URL for a specific Item or Collection
        :type item: bool
        """
        i = 0
        url = []
        current = cls
        while current:
            next = current.parent or None

            if current.resource_name:
                if not item and i == 0:
                    part = current.resource_name
                else:
                    exclude = True if not next and current.resource_exclude \
                        else False
                    part = current._item_url(resource_exclude=exclude)
            else:
                part = current.url

            if part and not part.startswith('/'):
                part = '/' + part
            url.append(part)
            i += 1
            current = next
        url.reverse()
        return ''.join(url) if url else None

    @property
    def item_url(self):
        """
        Get the URL for a item in this Controller
        """
        return self.get_url(item=True)

    @property
    def collection_url(self):
        """
        Return the collection URL for this Controller
        """
        return self.get_url()

    @classmethod
    def get_name(cls):
        """
        Get the Name of this Controller
        """
        name = cls.resource_key or cls.__name__
        return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'_\1',
                      name.lower())

    def _data(self, **kw):
        data = {}
        for k, v in kw.items():
            if v is not None:
                data[k] = v
        return data

    def _format_url(self, f_url, **f_data):
        LOG.debug("Formatting URL %s with data %s", f_url, f_data)
        try:
            return f_url % f_data
        except KeyError:
            msg = "Data (%s) insufficient to format (%s)" % (f_url, f_data)
            raise exceptions.LocalError(msg)

    def wrap_request(self, func, url=None, f_url=None, f_data=None,
                     *args, **kw):
        """
        Constructs the URL from the given arguments if it has a url and
        f_data. If only url is given then it just uses that.

        :param func: A function to be invoked.
                     Example: self.client.[get,list,update,delete,create]
        :type func: callable

        :param url: A URL or Format string
        :type url: string

        :param f_data: Data from which to construct the URL
        :type f_data: dict

        :param args: Arguments that's forwarded to the func
        :type args: list

        :param kw: Keywords to forward to func
        :type kw: dict / keywords

        :return: requests Response object
        :rtype: Response
        """
        if isinstance(f_data, dict):
            if not f_data.get('account_id') and self.client.account_id:
                f_data['account_id'] = self.client.account_id
            f_data['merchant_id'] = f_data['account_id']

        if f_data and 'account_id' in f_data:
            f_data['merchant_id'] = f_data.get('account_id')

        # NOTE: URL takes precedense over f_url
        if not url and f_url:
            # NOTE: Can this be changed?
            url = self._format_url(f_url, **f_data)
        elif not url:
            msg = 'No URL or URL Format String was passed'
            raise exceptions.LocalError(msg)

        response = func(url, *args, **kw)
        return response

    def _create(self, values, status_code=202, *args, **kw):
        """
        Create a new Resource from values
        """
        f_url = kw.pop('f_url', self.collection_url)
        response = self.wrap_request(
            self.client.post, f_url=f_url, data=json.dumps(values),
            status_code=status_code, *args, **kw)
        return response

    def _list(self, *args, **kw):
        """
        List objects of this Resource
        """
        f_url = kw.pop('f_url', self.collection_url)
        response = self.wrap_request(self.client.get, f_url=f_url, *args, **kw)
        return response

    def _get(self, *args, **kw):
        """
        Get a object of this Resource
        """
        f_url = kw.pop('f_url', self.item_url)
        response = self.wrap_request(self.client.get, f_url=f_url, *args, **kw)
        return response

    def _update(self, values, *args, **kw):
        """
        Update a Resource
        """
        f_url = kw.pop('f_url', self.item_url)
        response = self.wrap_request(
            self.client.update, f_url=f_url, data=json.dumps(values),
            *args, **kw)
        return response

    def _delete(self, status_code=204, *args, **kw):
        """
        Delete a Resource
        """
        f_url = kw.pop('f_url', self.item_url)
        response = self.wrap_request(
            self.client.delete, f_url=f_url, status_code=status_code,
            *args, **kw)
        return response


class Account(Base):
    resource_key = 'account'
    resource_name = 'merchants'

    def create(self, values):
        return self._create(values, url=self.collection_url).json

    def list(self):
        return self._list(url=self.collection_url).json

    def get(self, account_id):
        return self._get(f_data=self._data(account_id=account_id)).json

    def update(self, values, account_id=None):
        return self._get(f_data=self._data(account_id=account_id)).json

    def delete(self, account_id):
        return self._delete(f_data=self._data(account_id=account_id))


class Customer(Base):
    parent = Account
    resource_name = 'customers'

    def create(self, values, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._create(values, f_data=f_data).json

    def list(self, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._list(f_data=f_data).json

    def get(self, customer_id, account_id=None):
        f_data = self._data(account_id=account_id, customer_id=customer_id)

        return self._get(f_data=f_data).json

    def update(self, customer_id, values, account_id=None):
        f_data = self._data(account_id=account_id, customer_id=customer_id)

        return self._get(f_data=f_data).json

    def delete(self, customer_id, account_id=None):
        f_data = self._data(account_id=account_id, customer_id=customer_id)

        return self._delete(f_data=f_data)


class PaymentMethod(Base):
    parent = Customer
    resource_key = 'payment_method'
    resource_name = 'payment-methods'

    def create(self, customer_id, values, account_id=None):
        f_data = self._data(account_id=account_id, customer_id=customer_id)

        return self._create(values, f_data=f_data).json

    def list(self, customer_id, account_id=None):
        f_data = self._data(account_id=account_id, customer_id=customer_id)

        return self._list(f_data=f_data).json

    def get(self, customer_id, pm_id, account_id=None):
        f_data = self._data(
            account_id=account_id, customer_id=customer_id,
            payment_method_id=pm_id)

        return self._get(f_data=f_data).json

    def update(self, customer_id, pm_id, values, account_id=None):
        f_data = self._data(
            account_id=account_id, customer_id=customer_id,
            payment_method_id=pm_id)

        return self._get(f_data=f_data).json

    def delete(self, customer_id, pm_id, account_id=None):
        f_data = self._data(
            account_id=account_id, customer_id=customer_id,
            payment_method_id=pm_id)

        return self._delete(f_data=f_data)


class Product(Base):
    parent = Account
    resource_name = 'products'

    def create(self, values, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._create(values, f_data=f_data).json

    def list(self, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._list(f_data=f_data).json

    def get(self, product_id, account_id=None):
        f_data = self._data(account_id=account_id, product_id=product_id)

        return self._get(f_data=f_data).json

    def update(self, product_id, values, account_id=None):
        f_data = self._data(account_id=account_id, product_id=product_id)

        return self._get(f_data=f_data).json

    def delete(self, product_id, account_id=None):
        f_data = self._data(account_id=account_id, product_id=product_id)

        return self._delete(f_data=f_data).json


class Plan(Base):
    parent = Account
    resource_name = 'plans'

    def create(self, values, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._create(values, f_data=f_data).json

    def list(self, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._list(f_data=f_data).json

    def get(self, plan_id, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id)

        return self._get(f_data=f_data).json

    def update(self, plan_id, values, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id)

        return self._update(values, f_data=f_data).json

    def delete(self, plan_id, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id)

        return self._delete(f_data=f_data).json


class PlanItem(Base):
    parent = Plan
    resource_name = 'items'

    def create(self, plan_id, values, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id)

        return self._create(values, f_data=f_data).json

    def list(self, plan_id, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id)

        return self._list(f_data=f_data).json

    def get(self, plan_id, item_id, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id,
                            item_id=item_id)

        return self._get(f_data=f_data).json

    def update(self, plan_id, item_id, values, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id,
                            item_id=item_id)

        return self._update(values, f_data=f_data).json

    def delete(self, plan_id, item_id, account_id=None):
        f_data = self._data(account_id=account_id, plan_id=plan_id,
                            item_id=item_id)

        return self._delete(f_data=f_data).json


class Subscription(Base):
    parent = Account
    resource_name = 'subscriptions'

    def create(self, values, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._create(values, f_data=f_data).json

    def list(self, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._list(f_data=f_data).json

    def get(self, subscription_id, account_id=None):
        f_data = self._data(account_id=account_id,
                            subscription_id=subscription_id)

        return self._get(f_data=f_data).json

    def update(self, subscription_id, values, account_id=None):
        f_data = self._data(account_id=account_id,
                            subscription_id=subscription_id)

        return self._update(values, f_data=f_data).json

    def delete(self, subscription_id, account_id=None):
        f_data = self._data(account_id=account_id,
                            subscription_id=subscription_id)

        return self._delete(f_data=f_data).json


class Usage(Base):
    parent = Account
    resource_name = 'usages'

    def create(self, values, account_id=None):
        f_data = self._data(account_id=account_id)

        return self._create(values, f_data=f_data).json

    def list(self, account_id=None):
        f_data = self._data(account_id=account_id)
        return self._list(f_data=f_data).json

    def get(self, subscription_id, account_id=None):
        f_data = self._data(account_id=account_id,
                            subscription_id=subscription_id)
        return self._get(f_data=f_data).json

    def update(self, subscription_id, values, account_id=None):
        f_data = self._data(account_id=account_id,
                            subscription_id=subscription_id)

        return self._update(values, f_data=f_data).json

    def delete(self, subscription_id, account_id=None):
        f_data = self._data(account_id=account_id,
                            subscription_id=subscription_id)

        return self._delete(f_data=f_data).json


__all__ = [Account, Customer, PaymentMethod, Product, Plan, PlanItem,
           Subscription]
