class CommandApi(object):
    def __init__(self, client):
        self.client = client

    @classmethod
    def _add_id(cls, parser):
        parser.add_argument('id')

    # Merchant commands
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

    def merchant_list(self, parsed_args, command):
        return self.client.merchant.list()

    @staticmethod
    def merchant_get_parser(parser):
        parser.add_argument('id')

    def merchant_get(self, parsed_args, command):
        return self.client.merchant.get(parsed_args.id)

    @staticmethod
    def merchant_update_parser(parser):
        parser.add_argument('id')
        parser.add_argument('--language')
        parser.add_argument('--currency')

    def merchant_update(self, parsed_args, command):
        """
        Update a Merchant
        """
        values = dict(
            email=parsed_args.email,
            currency=parsed_args.currency)
        return self.client.merchant.update(parsed_args.id, values)

    @staticmethod
    def merchant_delete_parser(parser):
        parser.add_argument('id')

    def merchant_delete(self, parsed_args, command):
        return self.client.merchant.delete(parsed_args.id)

    # Customer commands
    @staticmethod
    def customer_create_parser(parser):
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--email')
        parser.add_argument('--currency', default='NOK')

    def customer_create(self, parsed_args, command):
        values = dict(
            username=parsed_args.username,
            password=parsed_args.password,
            email=parsed_args.email,
            currency=parsed_args.currency)
        return self.client.customer.create(values)

    @staticmethod
    def customer_list_parser(parser):
        parser.add_argument('merchant_id')

    def customer_list(self, parsed_args, command):
        return self.client.customer.list(parsed_args.merchant_id)

    @staticmethod
    def customer_get_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('id')

    def customer_get(self, parsed_args, command):
        return self.client.customer.get(parsed_args.merchant_id, parsed_args.id)

    @staticmethod
    def customer_update_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('id')

    def customer_update(self, parsed_args, command):
        values = dict(
            password=parsed_args.password,
            email=parsed_args.email,
            currency=parsed_args.currency)

        return self.client.customer.update(
            parsed_args.merchant_id,
            parsed_args.id,
            values)

    @staticmethod
    def customer_delete_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('id')

    def customer_delete(self, parsed_args, command):
        return self.client.customer.delete(parsed_args.merchant_id, parsed_args.id)

    # Product commands
    @staticmethod
    def product_create_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('name')
        parser.add_argument('type')
        parser.add_argument('measure')
        parser.add_argument('--title')
        parser.add_argument('--description')

    def product_create(self, parsed_args, command):
        values = dict(
            name=parsed_args.name,
            type=parsed_args.type,
            measure=parsed_args.measure,
            title=parsed_args.title,
            description=parsed_args.description
        )
        return self.client.product.create(values)

    @staticmethod
    def product_list_parser(parser):
        parser.add_argument('merchant_id')

    def product_list(self, parsed_args, command):
        return self.client.product.list(parsed_args.merchant_id)

    @staticmethod
    def product_get_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('id')

    def product_get(self, parsed_args, command):
        """
        Fetch a product
        """
        return self.client.product.get(parsed_args.merchant_id, parsed_args.id)

    @staticmethod
    def product_update_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('id')
        parser.add_argument('--name')
        parser.add_argument('--type')
        parser.add_argument('--measure')
        parser.add_argument('--title')
        parser.add_argument('--description')

    def product_update(self, parsed_args, command):
        """
        Update a product
        """
        values = dict(
            name=parsed_args.name,
            type=parsed_args.type,
            measure=parsed_args.measure,
            title=parsed_args.title,
            description=parsed_args.description
        )
        return self.client.product.update(
            parsed_args.merchant_id,
            parsed_args.id,
            values)

    @staticmethod
    def product_delete_parser(parser):
        parser.add_argument('merchant_id')
        parser.add_argument('id')

    def product_delete(self, parsed_args, command):
        """
        Update a product
        """
        return self.client.product.delete(parsed_args.merchant_id, parsed_args.id)
