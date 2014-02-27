from app import db
import settings

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    app_username = db.Column(db.String(255), unique=True)
    app_password = db.Column(db.String(255))

    def __init__(self, app_username='', app_password=''):
        self.app_username = app_username
        self.app_password = app_password

    def dictify(self):
        d = {}
        d['id'] = self.id
        d['app_username'] = self.app_username
        d['app_password'] = self.app_password
        return d

    def stringify(self):
        return str(self.dictify())

class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('users.id'))
    user = db.relationship('User')

    _redirect_urls = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_urls(self):
        if self._redirect_urls:
            return self._redirect_urls.split()
        return []

    @property
    def default_redirect_url(self):
        return self.redirect_urls[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

