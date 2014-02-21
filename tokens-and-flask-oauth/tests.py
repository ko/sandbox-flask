import os
import unittest
import tempfile
import base64
import json

from app import app,db

class AppTestCase(unittest.TestCase):

    def setUp(self):
        print '--- db setup ---' 

        db.create_all()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app2 = app.test_client()
        self.app_token = None

        print ''

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        print ''

    
    def login_user1(self):
        data={
            'username':'user1',
            'password':'pass1',
        }   
        headers = [('Content-Type', 'application/json')]
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))

        rv = self.app.open('/api/user/add',
            method='POST',
            headers=headers,
            data=json_data,
            follow_redirects=True)

        assert 'user1' in rv.data
        assert 'user2' not in rv.data

        rv = self.app.get('/api/user/1')

        assert 'user1' in rv.data
        assert 'user2' not in rv.data

    def request(self, test_client, method, url, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode(auth[0] + ':' + auth[1])

        kwargs['headers'] = headers

        return test_client.open(url, method=method, **kwargs)


    def test_index_page(self):
        rv = self.app.get('/')
        assert 'index page' in rv.data

    def test_user_add(self):
        self.login_user1()

    def test_user1_basic(self):
        self.login_user1()

        method = 'GET'
        url = '/api/user/secret'
        username = 'user1'
        password = 'pass1'

        rv = self.request(self.app, method, url, auth=(username,password))

        assert 'user1' in rv.data


    def test_get_token_user1(self):
        self.login_user1()

        method = 'GET'
        url = '/api/user/token'
        username = 'user1'
        password = 'pass1'

        rv = self.request(self.app, method, url, auth=(username,password))
        assert 'token' in rv.data

        token = json.loads(rv.data)['token']
        url = '/api/user/secret'

        rv = self.request(self.app2, method, url)
        assert 'Unauthorized' in rv.data

        rv = self.request(self.app2, method, url, auth=(token,'none'))
        assert 'user1' in rv.data


if __name__ == '__main__':
    unittest.main()
