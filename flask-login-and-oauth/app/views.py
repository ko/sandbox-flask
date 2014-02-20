from flask import redirect, url_for, request, session, abort
from flask.ext.login import login_user, logout_user, login_required, current_user

import app as mainapp
from app import app, db, facebook, login_manager
from models import Account

from base64 import b64decode, b64encode

import settings


###########################


def create_user_facebook(facebook_id, facebook_token):
    account = Account(facebook_id=facebook_id, facebook_token=facebook_token)
    db.session.add(account)
    db.session.commit()

    # XXX no account.id pk until the first commit.
    # so we generate_auth_token and recommit
    db.session.add(account)
    db.session.commit()

    return account


###########################


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):

    next_url = request.args.get('next') or url_for('secret')

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me')

    account = Account.query.filter_by(facebook_id = me.data['id']).first()
    if account is None:
        account = create_user_facebook(facebook_id=me.data['id'], 
                facebook_token=resp['access_token'])
    else:
        # TODO don't generate the token _every_ time...
        # XXX check if expired? or keep that in header_loader?
        #account.generate_auth_token()
        db.session.add(account)
        db.session.commit()

    login_user(account)

    return redirect(next_url)


###########################


@app.route('/login')
def login():
    callback=url_for('facebook_authorized', \
            next=request.args.get('next') or request.referrer or None, \
            _external=True)
    return facebook.authorize(callback)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/facebook', methods = ['POST'])
def login_facebook():
    if request.method != 'POST':
        return abort(405) # method not allowed

    """
    With the facebook_{id,token}, find or create a new
    Account as necessary and return the app_token. Don't
    wait for a second call to /token because that has a
    @login_required decorator. Chicken and egg.

    NB: Need to authorize this with actual facebook... or
    verify that this isn't fake information somehow. Don't
    trust the callers.
    """
    facebook_id = request.json.get('facebook_id')
    if facebook_id is None:
        abort(400)

    facebook_token = request.json.get('facebook_token')
    if facebook_token is None:
        abort(400)

    account = Account.query.filter_by(facebook_token = facebook_token).first() 
    if account is None:
        """
        So if someone can guess a facebook_{id,token} they can
        log in as them. That's cool! (omg)
        """
        account = create_user_facebook(facebook_id, facebook_token)

    print account.facebook_token
    # TODO omg
    login_user(account)

    return redirect(url_for('token'))


###########################


@app.route('/secret')
@login_required
def secret():
    return 'secret reveal: %s' % \
            (current_user.stringify())

# XXX is there value in this apart from testing?
@app.route('/token')
@login_required
def token():
    return str(current_user.get_app_token())

@app.route('/')
def index():
    return 'index page'


###########################


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run()




