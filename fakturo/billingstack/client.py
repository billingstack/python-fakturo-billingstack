import logging

from fakturo.core import client
from fakturo.billingstack import auth, resource


LOG = logging.getLogger(__name__)


class Client(client.BaseClient):
    def __init__(self, url='http://localhost:9090/billingstack', **kw):
        super(Client, self).__init__(url)

        # NOTE: Helper object that's set on requests.auth
        self.requests.auth = auth.AuthHelper(url, **kw)

        resources = resource.__all__
        LOG.debug('Loading Controllers: %s' % [c.get_name() for c in resources])

        for cls in resources:
            setattr(self, cls.get_name(), cls(self))

    @property
    def account_id(self):
        return self.requests.auth.account.get('id') \
            if self.requests.auth.account else None

    @property
    def customer_id(self):
        return self.requests.auth.customer.get('id') if \
            self.requests.auth.customer else None
