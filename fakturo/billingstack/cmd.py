class CommandApi(object):
    def __init__(self, client):
        self.client = client

    def merchant_list(self, parsed_args, command):
        return self.client.merchant.list()

    @staticmethod
    def merchant_create_parser(parser):
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--email')
        parser.add_argument('--currency', default='NOK')

    def merchant_create(self, parsed_args, command):
        values = dict(
            username=parsed_args.username,
            password=parsed_args.password,
            email=parsed_args.email,
            currency=parsed_args.currency
        )
        return self.client.merchant.create(values)
