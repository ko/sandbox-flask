from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    facebook_id = db.Column(db.Integer, unique=True)
    facebook_token = db.Column(db.String(255))

    def __init__(self, facebook_id, facebook_token):
        self.facebook_id = facebook_id
        self.facebook_token = facebook_token

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True
