import unittest
import json

from example_notes2 import app

class ExampleNotes2Test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        self.app = None

    def request(self, test_client, method, url, auth=None, **kwargs):
        headers = kwargs.get('headers',{})
        data = kwargs.get('data',{})

        if data:
            headers['Content-Type'] = 'application/json'
            json_data = json.dumps(data)
            json_data_length = len(json_data)
            headers['Content-Length'] = json_data_length
            kwargs['data'] = json_data

        kwargs['headers'] = headers

        return test_client.open(url, method=method, **kwargs)
    
    def test_index_get(self):
        api_url = '/'
        method = 'GET'

        rv = self.request(self.app, method, api_url)
        assert '{"1": "value1"}' in rv.data

    def test_index_post(self):
        api_url = '/'
        method = 'POST'
        data = { 'key':'value8',}

        rv = self.request(self.app, method, api_url, data=data)
        print rv.data
        assert '{"1": "value1", "2": "value8"}' in rv.data


if __name__=='__main__':
    unittest.main()
