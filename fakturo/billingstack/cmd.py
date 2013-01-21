class CommandApi(object):
    def __init__(self, client):
        self.client = client

    # account commands
    @staticmethod
    def account_create_parser(parser):
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--email')
        parser.add_argument('--currency', default='NOK')

    def account_create(self, args, command):
        values = dict(
            username=args.username,
            password=args.password,
            email=args.email,
            currency=args.currency
        )
        return self.client.account.create(values)

    def account_list(self, args, command):
        return self.client.account.list()

    @staticmethod
    def account_get_parser(parser):
        parser.add_argument('--account-id', required=True)

    def account_get(self, args, command):
        return self.client.account.get(account_id=args.id)

    @staticmethod
    def account_update_parser(parser):
        parser.add_argument('--account-id', required=True)
        parser.add_argument('--language')
        parser.add_argument('--currency')

    def account_update(self, args, command):
        """
        Update a account
        """
        values = dict(
            email=args.email,
            currency=args.currency)
        return self.client.account.update(values, account_id=args.account_id)

    @staticmethod
    def account_delete_parser(parser):
        parser.add_argument('id')

    def account_delete(self, args, command):
        return self.client.account.delete(args.id)

    # Customer commands
    @staticmethod
    def customer_create_parser(parser):
        parser.add_argument('--username')
        parser.add_argument('--password')
        parser.add_argument('--email')
        parser.add_argument('--currency', default='NOK')

    def customer_create(self, args, command):
        values = dict(
            username=args.username,
            password=args.password,
            email=args.email,
            currency=args.currency)
        return self.client.customer.create(values)

    @staticmethod
    def customer_list_parser(parser):
        parser.add_argument('--account-id')

    def customer_list(self, args, command):
        return self.client.customer.list(account_id=args.account_id)

    @staticmethod
    def customer_get_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def customer_get(self, args, command):
        return self.client.customer.get(args.id, account_id=args.account_id)

    @staticmethod
    def customer_update_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def customer_update(self, args, command):
        values = dict(
            password=args.password,
            email=args.email,
            currency=args.currency)

        return self.client.customer.update(
            args.id, values, account_id=args.account_id)

    @staticmethod
    def customer_delete_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def customer_delete(self, args, command):
        return self.client.customer.delete(args.id, account_id=args.account_id)

    # Plan comamnds
    @staticmethod
    def plan_create_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('--name')

    def plan_create(self, args, command):
        values = dict(name=args.name)
        return self.client.plan.create(values, account_id=args.account_id)

    @staticmethod
    def plan_list_parser(parser):
        parser.add_argument('--account-id')

    def plan_list(self, args, command):
        return self.client.plan.list(account_id=args.account_id)

    @staticmethod
    def plan_get_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argoment('id')

    def plan_get(self, args, command):
        return self.client.plan.get(args.id, account_id=args.account_id)

    @staticmethod
    def plan_update_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')
        parser.add_argument('--name')

    def plan_update(self, args, command):
        values = dict(name=args.name)
        return self.client.plan.delete(args.id, values, account_id=args.account_id)

    @staticmethod
    def plan_delete_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def plan_delete(self, args, command):
        return self.client.plan.delete(args.id, account_id=args.account_id)

    # Product commands
    @staticmethod
    def product_create_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')
        parser.add_argument('name')
        parser.add_argument('type')
        parser.add_argument('measure')
        parser.add_argument('--title')
        parser.add_argument('--description')

    def product_create(self, args, command):
        values = dict(
            name=args.name,
            type=args.type,
            measure=args.measure,
            title=args.title,
            description=args.description
        )
        return self.client.product.create(values, account_id=args.account_id)

    @staticmethod
    def product_list_parser(parser):
        parser.add_argument('--account-id')

    def product_list(self, args, command):
        return self.client.product.list(account_id=args.account_id)

    @staticmethod
    def product_get_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def product_get(self, args, command):
        """
        Fetch a product
        """
        return self.client.product.get(args.id, account_id=args.account_id)

    @staticmethod
    def product_update_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')
        parser.add_argument('--name')
        parser.add_argument('--type')
        parser.add_argument('--measure')
        parser.add_argument('--title')
        parser.add_argument('--description')

    def product_update(self, args, command):
        """
        Update a product
        """
        values = dict(
            name=args.name,
            type=args.type,
            measure=args.measure,
            title=args.title,
            description=args.description
        )
        return self.client.product.update(
            args.id, values, account_id=args.account_id)

    @staticmethod
    def product_delete_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def product_delete(self, args, command):
        """
        Update a product
        """
        return self.client.product.delete(args.id, account_id=args.account_id)
