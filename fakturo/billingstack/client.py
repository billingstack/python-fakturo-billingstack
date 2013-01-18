import logging

from fakturo.core import client
from fakturo.core import exceptions
from fakturo.billingstack import auth, controller


LOG = logging.getLogger(__name__)


class Client(client.BaseClient):
    def __init__(self, url=None, username=None, password=None, merchant=None):
        super(Client, self).__init__(url)
        auth_helper = auth.AuthHelper(url, username=username, password=password,
                                      merchant=merchant)
        self.requests.auth = auth_helper

        ctrls = controller.__all__
        LOG.debug('Loading Controllers: %s' % [c.get_name() for c in ctrls])

        for cls in ctrls:
            setattr(self, cls.get_name(), cls(self))

    def wrap_api_call(self, func, *args, **kw):
        """
        Wrap a self.<rest function> with exception handling

        :param func: The function to wrap
        """
        response = func(*args, **kw)
        if response.status_code != 200:
            error = None

            if response.json:
                error = response.json.get('error', None)
            if not error:
                error = 'Remote errorcode %i' % response.status_code
            raise exceptions.RemoteError(error)
        return response


