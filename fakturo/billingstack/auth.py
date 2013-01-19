import logging
import simplejson as json

from requests.auth import AuthBase

from fakturo.core import client


LOG = logging.getLogger(__name__)


class AuthHelper(AuthBase, client.BaseClient):
    def __init__(self, url, username=None, password=None,
                 merchant_name=None, customer_name=None):
        super(AuthHelper, self).__init__(url)

        self.auth_info = {}

        if not merchant_name and customer_name:
            raise ValueError('Customer set but not Merchant')

        cred_info = {
            'username': username,
            'password': password,
            'merchant': merchant_name,
            'customer': customer_name
        }

        self.cred_info = cred_info

        if self.cred_valid:
            self.refresh_auth()

    @property
    def cred_valid(self):
        c = self.cred_info
        return True if c.get('username') and c.get('password') else False

    def get_token_key(self, key):
        """
        Return something from the token info, None if no key or no info is there

        :param key: What to get
        """
        token_info = self.auth_info.get('token')
        return token_info.get('id') if token_info else token_info

    @property
    def token(self):
        return self.get_token_key('id')

    @property
    def endpoint(self):
        return self.auth_info.get('endpoint')

    @property
    def merchant(self):
        return self.auth_info.get('merchant')

    @property
    def customer(self):
        return self.auth_info.get('customer')

    def __call__(self, request):
        if not self.token and self.cred_valid:
            self.refresh_auth()
        request.headers['X-Auth-Token'] = self.token
        return request

    def refresh_auth(self):
        LOG.debug('Authenticating on URL %s info %s' % (self.url, self.cred_info))
        auth_data = dict([(k, v) for k, v in self.cred_info.items() if v])
        response = self.post('/authenticate', data=json.dumps(auth_data))
        self.auth_info.update(response.json)
