import os
import unittest
import tempfile
from app import app,db

class AppTestCase(unittest.TestCase):

    def setUp(self):
        print '--- db setup ---' 

        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        db.create_all()
        app.config['TESTING'] = True
        self.app = app.test_client()

        print ''

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

        print ''


    def test_index_page(self):
        print '--- test: index page ---'

        rv = self.app.get('/')
        assert 'index page' in rv.data

    def test_facebook_login(self):
        print '--- test: facebook login ---'

        rv = self.app.get('/login')
        assert '<title>Redirecting...</title>' in rv.data

if __name__ == '__main__':
    unittest.main()
