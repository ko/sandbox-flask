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

        print ''

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        print ''


    def test_index_page(self):
        print '--- test: index page ---'

        rv = self.app.get('/')
        assert 'index page' in rv.data

    def get_facebook_login_token(self, facebook_id, facebook_token):
        print '--- test: facebook login ---'
        data={
            'facebook_id':facebook_id,
            'facebook_token':facebook_token,
        }
        headers = [('Content-Type', 'application/json')]
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))

        rv = self.app.open('/login/facebook',
            method='POST',
            headers=headers,
            data=json_data
        )
        return rv.data

    def open_with_token(self, url, method, token):
        password='nop'
        return self.app.open(url, method=method,
                headers={
                    'Authorization': 'Basic ' + base64.b64encode(
                        token + ':' + password)
                }
        )

    def test_facebook_login(self):
        app_token = self.get_facebook_login_token('12345','09876')

        rv = self.open_with_token('/token', 'GET', app_token)
        assert rv.data == app_token
      

if __name__ == '__main__':
    unittest.main()
