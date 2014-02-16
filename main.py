from flask import Flask, redirect, request, session, url_for, render_template
from flask_oauth import OAuth

import settings

from helper import authenticated


## Login


def index():
    return render_template('index.html')

@authenticated
def secret():
    return render_template('secret.html')


############# v oauth setup v #############

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

############# ^ oauth setup ^ #############



############ v facebook login v ############

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me')

    return 'Logged in as id=%s name=%s redirect=%s' % \
            (me.data['id'], me.data['name'], request.args.get('next'))

############ ^ facebook login ^ ############



######### v facebook api v ##########

def facebook_friends():
    friends = facebook.get('/me/friends')

    return str(friends.data)


########## ^ facebook api ^ ############




################ v logout v ###############

def logout():
    pop_login_session()
    return redirect(url_for('index'))

################ ^ logout ^ ###############



############### v main v ##################

def generate_app():
    app = Flask(__name__)

    app.secret_key = settings.SECRET_KEY

    app.route('/')(index)
    app.route('/secret')(secret)

    app.route('/login/facebook')(facebook_login)
    app.route('/logout')(logout)
    app.route('/login/facebook/authorized')(facebook_authorized)
    app.route('/friends')(facebook_friends)

    return app


"""
Need to be publicly visible so that index.py can
import it ...
"""
app = generate_app()


if __name__ == "__main__":
    app.debug = True
    app.run()




