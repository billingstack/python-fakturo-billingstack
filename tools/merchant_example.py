
import logging
from fakturo.billingstack.client import Client

logging.basicConfig(level=logging.DEBUG)

client = Client('http://localhost:6543/v1')

for account in client.account.list():
    print "== %s ==" % account['name']
    for k, v in account.items():
        if not k == 'name':
            print "INFO", k, v
