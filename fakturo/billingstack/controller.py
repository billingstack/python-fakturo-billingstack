import simplejson as json


class Base(object):
    def __init__(self, client):
        self.client = client


class Merchant(Base):
    def create(self, values):
        response = self.client.post('/merchants', data=json.dumps(values))
        return response.json

    def list(self):
        response = self.client.get('/merchants')
        return response.json

    def get(self, id_):
        response = self.client.get('/%s' % id_)
        return response.json

    def update(self, id_, values):
        response = self.client.update('/%s' % id_, data=json.dumps(values))
        return response.json

    def delete(self, id_):
        self.client.delete('/%s' % id_)


class Customer(Base):
    def create(self, merchant_id, values):
        response = self.client.post('/%s/customers' % merchant_id,
                                    data=json.dumps(values))
        return response.json

    def list(self, merchant_id):
        response = self.client.get('/%s/customers' % merchant_id)
        return response.json

    def get(self, merchant_id, id_):
        response = self.client.get('/%s/customers/%s' % (merchant_id, id_))
        return response.json

    def update(self, merchant_id, id_, values):
        response = self.client.update('/%s/customers/%s' % (merchant_id, id_), data=json.dumps(values))
        return response.json

    def delete(self, merchant_id, id_):
        self.client.delete('/%s/customers/%s' % (merchant_id, id_))


class Product(Base):
    def create(self, merchant_id, values):
        response = self.client.post('/%s/products' % merchant_id,
                                    data=json.dumps(values))
        return response.json

    def list(self, merchant_id):
        response = self.client.get('/%s/products' % merchant_id)
        return response.json

    def get(self, merchant_id, id_):
        response = self.client.get('/%s/products/%s' % (merchant_id, id_))
        return response.json

    def update(self, merchant_id, id_, values):
        response = self.client.update('/%s/products/%s' % (merchant_id, id_), data=json.dumps(values))
        return response.json

    def delete(self, merchant_id, id_):
        self.client.delete('/%s/products/%s' % (merchant_id, id_))
