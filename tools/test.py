from fakturo.billingstack.client import Client


client = Client('http://localhost:9090/billingstack', username='ekarlso', password='secret0')
merchants = client.merchant.list()
