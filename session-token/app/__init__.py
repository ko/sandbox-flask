from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider

import settings



app = Flask(__name__)

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['DEBUG'] = settings.DEBUG

app.config['DATABASE_FILE'] = settings.DATABASE_FILE
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO

###########################


db = SQLAlchemy(app)

"""
In models.py we import 'db' from 'app'. So, we have
circular dependency here. Import 'Account' after 'db'
to temporarily resolve this.
"""
from models import User


###########################

oauth = OAuth2Provider(app)

@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # lol 10 second expiration
    expires = datetime.utcnow() + timedelta(seconds=10)
    grant = Grant(
            client_id=client_id,
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=current_user(),
            expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant

def current_user():
    if g.user and g.user.id:
        uid = g.user
        uid = session['id']
        return User.query.get(uid)
    return None



###########################


@app.before_first_request
def setup():
    db.create_all()


###########################

from app import views

