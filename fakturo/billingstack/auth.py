import logging
import simplejson as json

from requests.auth import AuthBase

from fakturo.core import client


LOG = logging.getLogger(__name__)


class AuthHelper(AuthBase, client.BaseClient):
    def __init__(self, url, username=None, password=None, merchant=None):
        super(AuthHelper, self).__init__(url)

        self.auth_info = {}

        self.username = username
        self.password = password
        self.merchant = merchant

        if self.creds_valid:
            self.refresh_auth()

    @property
    def creds(self):
        creds = dict(username=self.username, password=self.password)
        if self.merchant:
            creds['merchant'] = self.merchant
        return creds

    @property
    def creds_valid(self):
        return True if (self.username and self.password) else False

    @property
    def endpoint(self):
        return self.auth_info.get('endpoint', None)

    def get_token_key(self, key):
        """
        Return something from the token info, None if no key or no info is there

        :param key: What to get
        """
        token_info = self.auth_info.get('token', None)
        return token_info.get('id', None) if token_info else token_info

    @property
    def token(self):
        return self.get_token_key('id')

    def __call__(self, request):
        if not self.token and self.creds_valid:
            self.refresh_auth()
        request.headers['X-Auth-Token'] = self.token
        return request

    def refresh_auth(self):
        LOG.debug('Authenticating on URL %s info %s' % (self.url, self.creds))
        response = self.post('/authenticate', data=json.dumps(self.creds))
        self.auth_info.update(response.json)
