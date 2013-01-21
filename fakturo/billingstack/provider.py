from fakturo.core.provider import ProviderBase
from fakturo.billingstack.cmd import CommandApi
from fakturo.billingstack.client import Client


class BillingStackProvider(ProviderBase):
    api = CommandApi
    client = Client

    def get_api(self, parsed_args, cmd):
        opts = dict(
            url=cmd.app.options.api_url,
        )
        client = self.get_client(**opts)
        return self.api(client)
