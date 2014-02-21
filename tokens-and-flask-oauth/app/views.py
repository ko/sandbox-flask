from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.httpauth import HTTPBasicAuth

from app import app, db, facebook, auth
from models import User

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
    next_url = request.args.get('next') or url_for('get_user_secret')

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    facebook_token = (resp['access_token'], '')
    g.facebook_token = facebook_token
    me = facebook.get('/me')

    facebook_id = me.data['id']
    user = User.query.filter_by(facebook_id = facebook_id).first()
    if user is None:
        user = User(facebook_id=facebook_id, facebook_token=facebook_token)
        db.session.add(user)
        db.session.commit()
    else:
        # TODO don't generate the token _every_ time...
        # XXX check if expired? or keep that in header_loader?
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(next_url)


@app.route('/api/user/facebook/add', methods=['POST','GET'])
def user_add_facebook():
    callback=url_for('facebook_authorized', \
            next=request.args.get('next') or request.referrer or None, \
            _external=True)
    return facebook.authorize(callback)




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
    return jsonify({ 'username': g.user.app_username})

@app.route('/api/user/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify( {'token': token.decode('ascii')} )

@app.route('/')
def index():
    return 'index page'
