from flask import redirect, url_for, request, session
from flask.ext.login import login_user, logout_user, login_required, current_user

from app import app, db, facebook, login_manager
from models import Account


###########################


@login_manager.user_loader
def load_user(userid):
    return Account.query.filter_by(id=userid).first()

@login_manager.unauthorized_handler
def unauthorized(userid):
    return redirect(url_for('index'))


###########################


@facebook.tokengetter
def get_facebook_token():
#    if current_user.is_authenticated():
        return session.get('facebook_token')
#    else:
#        return None

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
        account = Account(facebook_id=me.data['id'], facebook_token=resp['access_token'])

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


###########################


@app.route('/secret')
@login_required
def secret():
    return 'secret reveal'

@app.route('/')
def index():
    return 'index page'


###########################


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run()




