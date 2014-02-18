from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db

import settings

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_username = db.Column(db.String(255), unique=True)
    app_token = db.Column(db.String(255))
    facebook_id = db.Column(db.Integer, unique=True)
    facebook_token = db.Column(db.String(255))

    def __init__(self, facebook_id, facebook_token):
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

    def generate_auth_token(self, expiration=600):
        s = Serializer(settings.SECRET_KEY, expires_in = expiration)
        app_token = s.dumps({ 'id': self.id }).decode('ascii')
        self.app_token = app_token
        return app_token
