from flask import Flask
from flask.ext.oauth import OAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import settings

app = Flask(__name__)

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['DEBUG'] = settings.DEBUG

app.config['DATABASE_FILE'] = settings.DATABASE_FILE
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO


###########################


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url = 'https://graph.facebook.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    authorize_url = 'https://www.facebook.com/dialog/oauth',
    consumer_key = settings.FACEBOOK_APP_ID,
    consumer_secret = settings.FACEBOOK_APP_SECRET,
    request_token_params = { 'scope': settings.FACEBOOK_APP_SCOPE }
)


###########################


login_manager = LoginManager()
login_manager.init_app(app)


###########################


db = SQLAlchemy(app)


###########################


from app import views

