from hashlib import sha1

from auth import login_serializer

from app import db

import settings

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_username = db.Column(db.String(255), unique=True)
    app_password = db.Column(db.String(255), unique=True)
    app_token = db.Column(db.String(255))
    facebook_id = db.Column(db.Integer, unique=True)
    facebook_token = db.Column(db.String(255))

    def __init__(self, app_username='', app_password='', facebook_id='', facebook_token=''):
        # TODO if app_username is empty, substitute with facebook_id (temporarily)
        self.app_username = app_username
        self.app_password = app_password
        self.facebook_id = facebook_id
        self.facebook_token = facebook_token

    def stringify(self):
        s = 'id=%s,app_token=%s,facebook_id=%s,' % \
                (self.id, self.app_token, self.facebook_id)
        return s

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_app_token(self):
        return self.app_token

    def get_auth_token(self):
        data = [str(self.id), self.app_username, sha1(self.app_password).hexdigest()]
        app_token = login_serializer.dumps(data)
        self.app_token = app_token
        return app_token

