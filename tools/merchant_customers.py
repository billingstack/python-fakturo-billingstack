
import logging
from fakturo.billingstack.client import Client

logging.basicConfig(level=logging.DEBUG)

client = Client('http://localhost:9090/billingstack', username='ekarlso', password='secret0')

for account in client.account.list():
    print client.customer.list(account['id'])
