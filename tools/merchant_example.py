
import logging
from fakturo.billingstack.client import Client

logging.basicConfig(level=logging.DEBUG)

client = Client('http://localhost:9090/billingstack', username='ekarlso', password='secret0', account_name='bouvet')

for account in client.account.list():
    print "== Merchant: %s==" % account['name']
    for k, v in account.items():
        if not k == 'name':
            print "INFO", k, v
