from app import db
import settings

class User(db.Model):
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


