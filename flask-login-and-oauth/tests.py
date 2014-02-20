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


    def test_index_page(self):
        print '--- test: index page ---'

        rv = self.app.get('/')
        assert 'index page' in rv.data

    def get_facebook_login_token(self, facebook_id, facebook_token):
        print '\n--- test: facebook login ---\n'
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
            data=json_data,
            follow_redirects=True
        )
        return rv.data

    def open_with_token(self, test_client, url, method, token):
        password='nop'

        userpass = token + ':' + password
        b64string = base64.b64encode(userpass)
        lenstr = len(b64string)

        print
        print '-----------------'
        print 'userpass | token | b64string | lenstr'
        print '-----------------'
        print userpass
        print token
        print b64string
        print lenstr
        print '-----------------'
        print
        
        return test_client.open(url, method=method,
                headers={
                    'Authorization': 'Basic ' + b64string
                }
        )



    def test_facebook_login(self):
        if self.app_token is None:
            app_token = self.get_facebook_login_token('12345','09876')
            self.app_token = app_token

        rv = self.open_with_token(self.app, '/token', 'GET', self.app_token)

        print '------'
        print ' test facebook login '
        print '-------'
        print str(rv)
        print '-------'

        assert rv.data == app_token

    def test_app_token_multiple_clients(self):
        if self.app_token is None:
            app_token = self.get_facebook_login_token('12345','098765')
            self.app_token = app_token
        assert self.app_token is not None

        assert self.app != self.app2
        assert self.app is not None
        rv = self.open_with_token(self.app, '/token', 'GET', self.app_token)
        print
        print '-----------------'
        print rv.data
        print '~~~~'
        print self.app_token
        print '-----------------'
        print
        assert rv.data == self.app_token

        assert self.app2 is not None
        rv = self.open_with_token(self.app2, '/token', 'GET', self.app_token)
        #assert rv.data == self.app_token

if __name__ == '__main__':
    unittest.main()
