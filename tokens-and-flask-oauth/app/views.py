from flask import Flask, abort, request, jsonify, g, url_for, redirect, make_response
from flask.ext.httpauth import HTTPBasicAuth
from base64 import b64encode

from app import app, db, facebook, auth
from models import User

"""
@facebook.tokengetter
def get_facebook_token():
    """
    if current_user.facebook_token is not None:
        return current_user.facebook_token
    """ 
    if g.facebook_token is not None:
        return g.facebook_token


@app.route('/api/user/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('get_auth_token')

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    facebook_token = (resp['access_token'], '')
    g.facebook_token = facebook_token
    me = facebook.get('/me')

    facebook_id = me.data['id'].decode('utf-8')

    user = User.query.filter_by(facebook_id = facebook_id).first()
    if user is None:
        user = User(facebook_id=facebook_id, facebook_token=facebook_token[0])
        db.session.add(user)
        db.session.commit()

    return redirect(next_url)
"""


def verify_facebook(facebok_id, facebook_token):
    me = facebook.get('/me')
    print str(me.data)

@app.route('/api/user/facebook/add', methods=['POST'])
def user_add_facebook():
    """
    callback=url_for('facebook_authorized', \
            next=request.args.get('next') or request.referrer or None, \
            _external=True)
    return facebook.authorize(callback)
    """
    fbid = request.json.get('facebook_id')
    fbtoken = request.json.get('facebook_token')

    if fbid is None or fbtoken is None:
        abort(400)
    user = User.query.filter_by(facebook_id = fbid).first()
    if user is None or not verify_facebook(fbid,fbtoken):
        abort(400)
    
    user = User(facebook_token=fbtoken, facebook_id=fbid)
    db.session.add(user)
    db.session.commit()

    return user.stringify()


@app.route('/api/user/add', methods=['POST'])
def user_add():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)
    if User.query.filter_by(app_username = username).first() is not None:
        abort(400)

    user = User(app_username = username)
    user.hash_pass(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({ 'username': user.app_username }), \
           201, \
           { 'Location': url_for('get_user', id = user.id, _external = True) }

@app.route('/api/user/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({ 'username': user.app_username})

@app.route('/api/user/secret')
@auth.login_required
def get_user_secret():
    if g.user is not None and g.user.app_username is not None:
        data = { 'username': g.user.app_username }
    return data

@app.route('/api/user/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify( {'token': token.decode('ascii')} )

@app.route('/')
def index():
    return 'index page'




