import requests
from urlparse import urlparse

from fakturo.core import exceptions
from fakturo.billingstack.controller import Merchant


class Client(object):
    def __init__(self, url=None, username=None, password=None):
        self.url = url

        def _ensure_url_hook(args):
            url_ = urlparse(args['url'])
            if not url_.scheme:
                args['url'] = url + url_.path

        headers = {'Content-Type': 'application/json'}

        hooks = dict(args=_ensure_url_hook)
        self.requests = requests.session(
            headers=headers,
            hooks=hooks
        )

        self.merchant = Merchant(self)

    def wrap_api_call(self, func, *args, **kw):
        """
        Wrap a self.<rest function> with exception handling

        :param func: The function to wrap
        """
        response = func(*args, **kw)
        if response.status_code != 200:
            error = response.json.get('error', 'Ooops')
            raise exceptions.RemoteError(error)
        return response

    def get(self, path, **kw):
        return self.wrap_api_call(self.requests.get, path, **kw)

    def post(self, path, **kw):
        return self.wrap_api_call(self.requests.post, path, **kw)

    def put(self, path, **kw):
        return self.wrap_api_call(self.requests.put, path, **kw)

    def delete(self, path, **kw):
        return self.wrap_api_call(self.requests.delete, path, **kw)
