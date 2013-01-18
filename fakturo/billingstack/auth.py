import logging
import simplejson as json

import requests
from requests.auth import AuthBase

from fakturo.core import exceptions, utils


LOG = logging.getLogger(__name__)


class AuthHelper(AuthBase):
    def __init__(self, url, username=None, password=None, merchant=None):
        self.url = url

        hooks = dict(pre_request=utils.log_request)
        self.requests = requests.session(hooks=hooks)

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
        response = self.requests.post(self.url + '/authenticate',
                                      data=json.dumps(self.creds))
        if response.status_code != 200:
            error = response.json.get('error', None)
            if not error:
                error = 'Remote error occured. Response Body:\n%s' % response.content
            raise exceptions.RemoteError(response.status_code, error)
        self.auth_info.update(response.json)
