import logging
import re
import simplejson as json


from fakturo.core.provider import resource


LOG = logging.getLogger(__name__)


class Base(resource.BaseResource):
    resource = None
    resource_exclude = False
    url = None

    parent = None

    @classmethod
    def _item_url(cls, resource_exclude=False):
        """
        Return the url part for a single resource of this class

        :return: URL For a Item
        :rtype: string
        """
        if cls.resource:
            part_id = '/' + '%(' + cls.resource[0:-1] + '_id)s'

            return  part_id if resource_exclude else '/' + cls.resource + part_id
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

            if current.resource:
                if not item and i == 0:
                    part = current.resource
                else:
                    exclude = True if not next and current.resource_exclude else False
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
        return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'_\1',
                      cls.__name__).lower()

    def wrap_request(self, func, url, url_data=None, *args, **kw):
        """
        Constructs the URL from the given arguments if it has a url and
        url_data. If only url is given then it just uses that.

        :param func: A function to be invoked.
                     Example: self.client.[get,list,update,delete,create]
        :type func: callable

        :param url: A URL or Format string
        :type url: string

        :param url_data: Data from which to construct the URL
        :type url_data: dict

        :param args: Arguments that's forwarded to the func
        :type args: list

        :param kw: Keywords to forward to func
        :type kw: dict / keywords

        :return: requests Response object
        :rtype: Response
        """
        if url_data != None:
            url = url % url_data
            LOG.debug('URL formatted to: %s' % url)

        if self.client.account_id:
            url = '/' + self.client.account_id + url

        response = func(url, *args, **kw)
        return response

    def _create(self, values, *args, **kw):
        """
        Create a new Resource from values
        """
        url = kw.pop('url', self.collection_url)
        response = self.wrap_request(
            self.client.post, url, data=json.dumps(values), *args, **kw)
        return response

    def _list(self, *args, **kw):
        """
        List objects of this Resource
        """
        url = kw.pop('url', self.collection_url)
        response = self.wrap_request(self.client.get, url, *args, **kw)
        return response

    def _get(self, *args, **kw):
        """
        Get a object of this Resource
        """
        url = kw.pop('url', self.item_url)
        response = self.wrap_request(self.client.get, url, *args, **kw)
        return response

    def _upate(self, values, *args, **kw):
        """
        Update a Resource
        """
        url = kw.pop('url', self.item_url)
        response = self.wrap_request(
            self.client.update, url, data=json.dumps(values), *args, **kw)
        return response

    def _delete(self, *args, **kw):
        """
        Delete a Resource
        """
        url = kw.pop('url', self.item_url)
        response = self.wrap_request(self.client.delete, url, *args, **kw)
        return response


class Account(Base):
    resource = 'merchants'
    resource_exclude = True

    def create(self, values):
        return self.create(values).json

    def list(self):
        return self._list().json

    def get(self, account_id):
        return self._get(locals()).json

    def update(self, account_id, values):
        return self._get(locals()).json

    def delete(self, account_id):
        return self._delete(locals()).json


class Customer(Base):
    parent = Account
    resource = 'customers'

    def create(self, account_id, customer_id, values):
        return self._create(locals(), values).json

    def list(self, account_id):
        return self._list(locals()).json

    def get(self, account_id, customer_id):
        return self._get(locals()).json

    def update(self, account_id, customer_id, values):
        return self._get(locals()).json

    def delete(self, account_id, customer_id):
        return self._delete(locals()).json


class Product(Base):
    parent = Account
    resource = 'products'

    def create(self, account_id, product_id, values):
        return self._create(locals(), values).json

    def list(self, account_id):
        return self._list(locals()).json

    def get(self, account_id, product_id):
        return self._get(locals()).json

    def update(self, account_id, product_id, values):
        return self._get(locals()).json

    def delete(self, account_id, product_id):
        return self._delete(locals()).json


class Plan(Base):
    parent = Account
    resource = 'plans'

    def create(self, account_id, values):
        return self._create(locals(), values).json

    def list(self, account_id):
        return self._list(locals()).json

    def get(self, account_id, plan_id):
        return self._get(locals()).json

    def update(self, account_id, plan_id, values):
        return self._get(locals()).json

    def delete(self, account_id, plan_id):
        return self._delete(locals()).json


class PlanItem(Base):
    parent = Plan
    resource = 'items'

    def create(self, account_id, plan_id, values):
        return self._create(locals(), values).json

    def list(self, account_id, plan_id):
        return self._list(locals()).json

    def get(self, account_id, plan_id, item_id):
        return self._get(locals()).json

    def update(self, account_id, plan_id, item_id, values):
        return self._get(locals()).json

    def delete(self, account_id, plan_id, item_id):
        return self._delete(locals()).json


class PlanItemRule(Base):
    parent = PlanItem
    resource = 'rules'

    def create(self, account_id, plan_id, item_id, values):
        return self._create(locals(), values).json

    def list(self, account_id, plan_id, item_id):
        return self._list(locals()).json

    def get(self, account_id, plan_id, item_id, rule_id):
        return self._get(locals()).json

    def update(self, account_id, plan_id, item_id, rule_id, values):
        return self._get(locals()).json

    def delete(self, account_id, plan_id, item_id, rule_id):
        return self._delete(locals()).json


class PlanItemRuleRange(Base):
    parent = PlanItemRule
    resource = 'ranges'

    def create(self, account_id, plan_id, item_id, rule_id, values):
        response = self.client.post(self.collection_url % locals(),
                                    data=json.dumps(values))
        return response.json

    def list(self, account_id, plan_id, item_id, rule_id):
        response = self.client.get(self.collection_url % locals())
        return response.json

    def get(self, account_id, plan_id, item_id, rule_id, range_id):
        response = self.client.get(self.item_url % locals())
        return response.json

    def update(self, account_id, plan_id, item_id, rule_id, range_id, values):
        response = self.client.update(self.item_url % locals(),
                                      data=json.dumps(values))
        return response.json

    def delete(self, account_id, plan_id, item_id, rule_id, range_id):
        self.client.delete(self.item_url % locals())


__all__ = [Account, Customer, Product, Plan, PlanItem, PlanItemRule, PlanItemRuleRange]
