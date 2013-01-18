import logging
import simplejson as json

import requests
from requests.auth import AuthBase

from fakturo.core import client, exceptions


LOG = logging.getLogger(__name__)


class AuthHelper(AuthBase, client.BaseClient):
    def __init__(self, url, username=None, password=None, merchant=None):
        self.url = url

        self.requests = self.get_requests()

        self.auth_info = {}

        creds = dict(username=username, password=password)
        if merchant:
            creds['merchant'] = merchant
        self.creds = creds

        if username and password:
            self.refresh_auth()

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
        if not self.token:
            self.refresh_auth()
        request.headers['X-Auth-Token'] = self.token
        return request

    def refresh_auth(self):
        LOG.debug('Authenticating on URL %s info %s' % (self.url, self.creds))
        response = self.post('/authenticate', data=json.dumps(self.creds))
        self.auth_info.update(response.json)
