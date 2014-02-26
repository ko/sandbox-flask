from flask import Flask, abort, request, jsonify, g, url_for, redirect

from app import app, db

from models import User


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
    data = { 'username': g.user.app_username }
    return jsonify(data)

@app.route('/api/user/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify( {'token': token.decode('ascii')} )

@app.route('/')
def index():
    return 'index page'




