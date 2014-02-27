from flask import Flask, g, before_first_request
from flask.ext.sqlalchemy import SQLAlchemy

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

def current_user():
    if g.user and g.user.id:
        uid = g.user
        uid = session['id']
        return User.query.get(uid)
    return None



###########################


@before_first_request
def setup():
    db.create_all()


###########################

from app import views

