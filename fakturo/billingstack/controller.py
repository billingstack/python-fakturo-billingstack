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
                part = current.resource or current.url

            if not part.startswith('/'):
                part = '/' + part

            reversed.append(part)
            current = next
            i += 1

        url = list(reversed)
        url.reverse()
        return ''.join(url)

    @property
    def item_url(self):
        """
        Get the URL for a item in this Controller
        """
        return self.get_url(item=True)

    @property
    def collection_url(self):
        return self.get_url()

    @classmethod
    def get_name(cls):
        return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'_\1',
                      cls.__name__).lower()

    def _wrap_api_call(self, func, url_string, url_data, *args, **kw):
        url = url_string % url_data
        LOG.debug('URL formatted to: %s' % url)
        response = func(url, *args, **kw)
        return response

    def _create(self, url_data, values):
        response = self._wrap_api_call(self.client.post, self.collection_url,
                                       url_data, data=json.dumps(values))
        return response

    def _list(self, url_data):
        response = self._wrap_api_call(self.client.list, self.collection_url,
                                       url_data)
        return response

    def _get(self, url_data):
        response = self._wrap_api_call(self.client.get, self.item_url, url_data)
        return response

    def _upate(self, url_data, values):
        response = self._wrap_api_call(self.client.update, self.item_url,
                                       url_data, data=json.dumps(values))
        return response

    def _delete(self, url_data):
        response = self._wrap_api_call(self.client.delete, self.item_url,
                                       url_data)
        return response


class Merchant(Base):
    url = '/%(merchant_id)s'

    def create(self, merchant_id, values):
        return self._create(locals(), values).json

    def list(self, merchant_id):
        return self._list(locals()).json

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
