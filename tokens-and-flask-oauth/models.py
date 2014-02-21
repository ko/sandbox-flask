from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer  as Serializer
from itsdangerous import BadSignature, SignatureExpired

from app import db
import settings

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_username = db.Column(db.String(255), unique=True)
    app_password = db.Column(db.String(255))
    facebook_id = db.Column(db.String(255), unique=True)
    facebook_token = db.Column(db.String(255), unique=True)

    def __init__(self, app_username='john doe', app_password='password', 
                 facebook_id='fbid', facebook_token='fbtoken'):
        self.app_username = app_username
        self.app_password = app_password
        self.facebook_id = facebook_id
        self.facebook_token = facebook_token

    def stringify(self):
        s = 'id=%s,app_username=%s,app_password=%s,' % \
                (self.id, self.app_username, self.app_password)
        s +='\n'
        s +='facebook_id=%s,facebook_token=%s' % \
                (self.facebook_id, self.facebook_token)
        return s

    def hash_pass(self, password):
        self.app_password = pwd_context.encrypt(password)

    def verify_pass(self, password):
        return pwd_context.verify(password, self.app_password)

    def generate_auth_token(self, expiration = 600):
        data = { 'id': self.id }
        s = Serializer(settings.SECRET_KEY, expires_in = expiration)
        return s.dumps(data)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid, expired
        except BadSignature:
            return None # invalid
        user = User.query.get(data['id'])
        return user



