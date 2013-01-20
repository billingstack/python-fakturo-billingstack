import logging
import re
import simplejson as json


LOG = logging.getLogger(__name__)


class Base(object):
    resource = None
    url = None

    parent = None

    def __init__(self, client):
        self.client = client

    @classmethod
    def _item_url(cls):
        """
        Return the url part for a single resource of this class

        :return: URL For a Item
        :rtype: string
        """
        if cls.resource:
            id_key = '%(' + cls.resource[0:-1] + '_id)s'
            return '/' + cls.resource + '/' + id_key
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
        reversed = []
        current = cls
        while current:
            next = current.parent or None
            if next:
                if not item and i == 0:
                    part = '/' + current.resource
                else:
                    part = current._item_url()
            else:
                part = current.resource
            if part:
                if not part.startswith('/'):
                    part = '/' + part
                reversed.append(part)
            i += 1
            current = next

        reversed.reverse()
        return ''.join(reversed) if reversed else None

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
        if url_data != None:
            url = url % url_data
            LOG.debug('URL formatted to: %s' % url)
        response = func(url, *args, **kw)
        return response

    def _create(self, values, *args, **kw):
        url = kw.pop('url', self.collection_url)
        response = self.wrap_request(
            self.client.post, url, data=json.dumps(values), *args, **kw)
        return response

    def _list(self, *args, **kw):
        url = kw.pop('url', self.collection_url)
        response = self.wrap_request(self.client.get, url, *args, **kw)
        return response

    def _get(self, *args, **kw):
        url = kw.pop('url', self.item_url)
        response = self.wrap_request(self.client.get, url, *args, **kw)
        return response

    def _upate(self, values, *args, **kw):
        url = kw.pop('url', self.item_url)
        response = self.wrap_request(
            self.client.update, url, data=json.dumps(values), *args, **kw)
        return response

    def _delete(self, *args, **kw):
        url = kw.pop('url', self.item_url)
        response = self.wrap_request(self.client.delete, url, *args, **kw)
        return response


class Merchant(Base):
    collection_url = '/merchants'
    item_url = collection_url + '/%(merchant_id)s'

    def create(self, values):
        return self.create(values).json

    def list(self):
        return self._list().json

    def get(self, merchant_id):
        return self._get(locals()).json

    def update(self, merchant_id, values):
        return self._get(locals()).json

    def delete(self, merchant_id):
        return self._delete(locals()).json


class Customer(Base):
    parent = Merchant
    resource = 'customers'

    def create(self, merchant_id, customer_id, values):
        return self._create(locals(), values).json

    def list(self, merchant_id):
        return self._list(locals()).json

    def get(self, merchant_id, customer_id):
        return self._get(locals()).json

    def update(self, merchant_id, customer_id, values):
        return self._get(locals()).json

    def delete(self, merchant_id, customer_id):
        return self._delete(locals()).json


class Product(Base):
    parent = Merchant
    resource = 'products'

    def create(self, merchant_id, product_id, values):
        return self._create(locals(), values).json

    def list(self, merchant_id):
        return self._list(locals()).json

    def get(self, merchant_id, product_id):
        return self._get(locals()).json

    def update(self, merchant_id, product_id, values):
        return self._get(locals()).json

    def delete(self, merchant_id, product_id):
        return self._delete(locals()).json


class Plan(Base):
    parent = Merchant
    resource = 'plans'

    def create(self, merchant_id, values):
        return self._create(locals(), values).json

    def list(self, merchant_id):
        return self._list(locals()).json

    def get(self, merchant_id, plan_id):
        return self._get(locals()).json

    def update(self, merchant_id, plan_id, values):
        return self._get(locals()).json

    def delete(self, merchant_id, plan_id):
        return self._delete(locals()).json


class PlanItem(Base):
    parent = Plan
    resource = 'items'

    def create(self, merchant_id, plan_id, values):
        return self._create(locals(), values).json

    def list(self, merchant_id, plan_id):
        return self._list(locals()).json

    def get(self, merchant_id, plan_id, item_id):
        return self._get(locals()).json

    def update(self, merchant_id, plan_id, item_id, values):
        return self._get(locals()).json

    def delete(self, merchant_id, plan_id, item_id):
        return self._delete(locals()).json


class PlanItemRule(Base):
    parent = PlanItem
    resource = 'rules'

    def create(self, merchant_id, plan_id, item_id, values):
        return self._create(locals(), values).json

    def list(self, merchant_id, plan_id, item_id):
        return self._list(locals()).json

    def get(self, merchant_id, plan_id, item_id, rule_id):
        return self._get(locals()).json

    def update(self, merchant_id, plan_id, item_id, rule_id, values):
        return self._get(locals()).json

    def delete(self, merchant_id, plan_id, item_id, rule_id):
        return self._delete(locals()).json


class PlanItemRuleRange(Base):
    parent = PlanItemRule
    resource = 'ranges'

    def create(self, merchant_id, plan_id, item_id, rule_id, values):
        response = self.client.post(self.collection_url % locals(),
                                    data=json.dumps(values))
        return response.json

    def list(self, merchant_id, plan_id, item_id, rule_id):
        response = self.client.get(self.collection_url % locals())
        return response.json

    def get(self, merchant_id, plan_id, item_id, rule_id, range_id):
        response = self.client.get(self.item_url % locals())
        return response.json

    def update(self, merchant_id, plan_id, item_id, rule_id, range_id, values):
        response = self.client.update(self.item_url % locals(),
                                      data=json.dumps(values))
        return response.json

    def delete(self, merchant_id, plan_id, item_id, rule_id, range_id):
        self.client.delete(self.item_url % locals())


__all__ = [Merchant, Customer, Product, Plan, PlanItem, PlanItemRule, PlanItemRuleRange]
