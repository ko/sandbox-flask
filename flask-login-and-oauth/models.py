from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    token = db.Column(db.String(255))
    secret = db.Column(db.String(255))

    def __init__(self, username, token, secret):
        self.username = username
        self.token = token
        self.secret = secret

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True
