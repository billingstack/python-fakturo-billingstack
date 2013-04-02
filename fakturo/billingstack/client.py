import logging

from fakturo.core import client
from fakturo.billingstack import auth, resource


LOG = logging.getLogger(__name__)


class Client(client.BaseClient):
    def __init__(self, url='http://localhost:9090/v1', username=None,
                 password=None, account_name=None, account_id=None, **kw):
        super(Client, self).__init__(url)

        auth_opts = dict(
            username=username,
            password=password
        )
        if account_name and not account_id:
            auth_opts['account_name'] = account_name
        elif account_id and not account_name:
            auth_opts['account_id'] = account_id

        # NOTE: Only setup auth if there's a username + password
        self._account_id = None
        if username and password:
            LOG.debug('Authentication info %s' % auth_opts)
            self.requests.auth = auth.AuthHelper(url, **auth_opts)
        elif account_id:
            self._account_id = account_id

        resources = resource.__all__
        LOG.debug('Loading Controllers: %s' % [c.get_name()
                  for c in resources])

        for cls in resources:
            setattr(self, cls.get_name(), cls(self))

    @property
    def account_id(self):
        if self.requests.auth:
            return self.requests.auth.account.get('id') \
                if self.requests.auth.account else None
        elif self._account_id:
            return self._account_id
