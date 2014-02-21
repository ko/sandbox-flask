from flask import Flask, g
from flask.ext.oauth import OAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

from itsdangerous import constant_time_compare, BadData

import settings



app = Flask(__name__)

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['DEBUG'] = settings.DEBUG

app.config['DATABASE_FILE'] = settings.DATABASE_FILE
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO

app.config['PERMANENT_SESSION_LIFETIME'] = settings.PERMANENT_SESSION_LIFETIME


###########################


db = SQLAlchemy(app)

"""
In models.py we import 'db' from 'app'. So, we have
circular dependency here. Import 'Account' after 'db'
to temporarily resolve this.
"""
from models import User


###########################


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(app_username = username_or_token).first()
        if not user or not user.verify_pass(password):
            return False
    g.user = user
    return True


###########################


from app import views

