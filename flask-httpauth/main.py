from flask import Flask, redirect, request, session, abort
from flask import url_for, render_template, g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

import settings

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DB_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = settings.SQLALCHEMY_COMMIT_ON_TEARDOWN


db = SQLAlchemy(app)
auth = HTTPBasicAuth()

user_whitelist = []

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        self.id = 1

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps( { 'id': self.id } )

    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid but expired
        except BadSignature:
            return None # invalid

        user = User(username = 'a')

        return user





@app.route('/')
def index():
    return 'index'





@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify( { 'token': token.decode('ascii') , 'duration': 600 } )


@app.route('/api/users/add', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)
    """
    if User.query.filter_by(username = username).first() is not None:
        abort(400)
    """
    if any(username in user.username for user in user_whitelist):
        abort(400)

    user = User(username = username)
    user.hash_password(password)

    user_whitelist.append(user)
    
    return jsonify({ 'username': user.username }), 201


@auth.verify_password
def verify_password(username_or_token, password):
    # try token first
    user = User.verify_auth_token(username_or_token)
    if not user:
        """
        # try user/pass
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
        """
        if not any(username_or_token in user.username for user in user_whitelist):
            return False
    user = User(username = username_or_token)
    user.hash_password(password)
    g.user = user
    return True


# NOTE order matters for decorators...
@app.route('/api/secret')
@auth.login_required
def secret():
    return jsonify( { 'data': 'secret for %s' % g.user.username } )

if __name__ == "__main__":
    app.debug = True
    app.run()




