from fakturo.core.provider import ProviderBase
from fakturo.billingstack.cmd import CommandApi
from fakturo.billingstack.client import Client


class BillingStackProvider(ProviderBase):
    api = CommandApi
    client = Client

    def get_api(self, parsed_args, cmd):
        opts = dict(
            url=cmd.app.options.api_url,
            username=cmd.app.options.username,
            password=cmd.app.options.password,
        )

        if cmd.app.options.account_id:
            opts['account_id'] = cmd.app.options.account_id
        elif cmd.app.options.account_name:
            opts['account_name'] = cmd.app.options.account_name

        client = self.get_client(**opts)
        return self.api(client)
