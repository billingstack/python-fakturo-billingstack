class CommandApi(object):
    def __init__(self, client):
        self.client = client

    # account commands
    @staticmethod
    def account_create_parser(parser):
        parser.add_argument('--name')
        parser.add_argument('--currency', default='NOK')
        parser.add_argument('--language', default='NOR')

    def account_create(self, args, command):
        values = dict(
            name=args.name,
            language=args.language,
            currency=args.currency
        )
        return self.client.account.create(values)

    def account_list(self, args, command):
        return self.client.account.list()

    @staticmethod
    def account_get_parser(parser):
        parser.add_argument('id')

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
            currency=args.currency,
            language=args.language)
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
        return self.client.plan.delete(
            args.id, values, account_id=args.account_id)

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

    # Subscription
    @staticmethod
    def subscription_create_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('plan_id')
        parser.add_argument('customer_id')
        parser.add_argument('payment_method_id')

        parser.add_argument('--billing_day')
        parser.add_argument('--resource_id')
        parser.add_argument('--resource_type')

    def subscription_create(self, args, command):
        values = dict(
            plan_id=args.plan_id,
            customer_id=args.customer_id,
            payment_method_id=args.payment_method_id,
            billing_day=args.billing_day,
            resource_id=args.resource_id,
            resource_type=args.resource_type
        )
        return self.client.subscription.create(
            values, account_id=args.account_id)

    @staticmethod
    def subscription_list_parser(parser):
        parser.add_argument('--account-id')

    def subscription_list(self, args, command):
        return self.client.subscription.list(
            account_id=args.account_id)

    @staticmethod
    def subscription_get_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def subscription_get(self, args, command):
        """
        Fetch a subscription
        """
        return self.client.subscription.get(
            args.id, account_id=args.account_id)

    @staticmethod
    def subscription_update_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')
        parser.add_argument('--billing_day')
        parser.add_argument('--resource_id')
        parser.add_argument('--resource_type')

    def subscription_update(self, args, command):
        """
        Update a subscription
        """
        values = dict(
            billing_day=args.billing_day,
            resource_id=args.resource_id,
            resource_type=args.resource_type,
        )
        return self.client.subscription.update(
            args.id, values, account_id=args.account_id)

    @staticmethod
    def subscription_delete_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('id')

    def subscription_delete(self, args, command):
        """
        Update a subscription
        """
        return self.client.subscription.delete(
            args.id, account_id=args.account_id)

    # PaymentMethod
    @staticmethod
    def payment_method_create_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('customer_id')
        parser.add_argument('customer_id')
        parser.add_argument('--name')
        parser.add_argument('--identifier')
        parser.add_argument('--expires')

    def payment_method_create(self, args, command):
        values = dict(
            name=args.name,
            identifier=args.identifier,
            expires=args.expires
        )

        return self.client.payment_method.create(
            args.customer_id, values, account_id=args.account_id)

    @staticmethod
    def payment_method_list_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('customer_id')

    def payment_method_list(self, args, command):
        return self.client.payment_method.list(
            args.customer_id, account_id=args.account_id)

    @staticmethod
    def payment_method_get_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('customer_id')
        parser.add_argument('id')

    def payment_method_get(self, args, command):
        """
        Fetch a payment_method
        """
        return self.client.payment_method.get(
            args.customer_id, args.id, account_id=args.account_id)

    @staticmethod
    def payment_method_update_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('customer_id')
        parser.add_argument('id')
        parser.add_argument('--billing_day')
        parser.add_argument('--resource_id')
        parser.add_argument('--resource_type')

    def payment_method_update(self, args, command):
        """
        Update a payment_method
        """
        values = dict(
            billing_day=args.billing_day,
            resource_id=args.resource_id,
            resource_type=args.resource_type,
        )
        return self.client.payment_method.update(
            args.id, values, account_id=args.account_id)

    @staticmethod
    def payment_method_delete_parser(parser):
        parser.add_argument('--account-id')
        parser.add_argument('customer_id')
        parser.add_argument('id')

    def payment_method_delete(self, args, command):
        """
        Update a payment_method
        """
        return self.client.payment_method.delete(
            args.customer_id, args.id, account_id=args.account_id)
