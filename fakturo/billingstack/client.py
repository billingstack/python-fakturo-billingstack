import logging

from fakturo.core import client
from fakturo.billingstack import auth, controller


LOG = logging.getLogger(__name__)


class Client(client.BaseClient):
    def __init__(self, url=None, **kw):
        super(Client, self).__init__(url)

        # NOTE: Helper object that's set on requests.auth
        self.requests.auth = auth.AuthHelper(url, **kw)

        ctrls = controller.__all__
        LOG.debug('Loading Controllers: %s' % [c.get_name() for c in ctrls])

        for cls in ctrls:
            setattr(self, cls.get_name(), cls(self))

    @property
    def merchant_id(self):
        return self.requests.auth.merchant.get('id') \
            if self.requests.auth.customer else None

    @property
    def customer_id(self):
        return self.requests.auth.customer.get('id') if \
            self.requests.auth.customer else None
