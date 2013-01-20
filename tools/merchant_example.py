
import logging
from fakturo.billingstack.client import Client

logging.basicConfig(level=logging.DEBUG)

client = Client('http://localhost:9090/billingstack', username='ekarlso', password='secret0')

for merchant in client.merchant.list():
    print "== Merchant: %s==" % merchant['name']
    for k, v in merchant.items():
        if not k == 'name':
            print "INFO", k, v
