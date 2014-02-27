from flask import Flask, abort, request, jsonify, g, url_for, redirect
from werkzeug.security import gen_salt

from app import app, db

from models import User


@app.route('/client')
def client():
    user = current_user()
    if not user:
        return 'not user?'
    item = Client(
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_urls='http://localhost:8000/authorized',
            _default_scopes='email',
            user_id=user.id,
    )
    db.session.add(item)
    db.session.commit()

    return jsonify(
            client_id=item.client_id,
            client_secret=item.client_secret,
    )

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

    g.user = user

    return jsonify(user.dictify())

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




