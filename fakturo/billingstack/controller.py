import simplejson as json


class Base(object):
    def __init__(self, client):
        self.client = client


class Merchant(Base):
    def create(self, merchant):
        response = self.client.post('/merchants', data=json.dumps(merchant))
        return response.json

    def list(self):
        response = self.client.get('/merchants')
        return response.json
