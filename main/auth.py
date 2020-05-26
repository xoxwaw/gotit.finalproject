import os
import datetime as dt
from functools import wraps

import jwt
from jwt.exceptions import InvalidSignatureError
from flask import request, jsonify

from main.config.base import BaseEnv
from main.models.user import UserModel
from main.libs.password import verify_password

algorithm = 'HS256'
secret = BaseEnv.SECRET_KEY


def encode_jwt(user_id):
    """encode payload to a jwt"""
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(days=0, hours=1),
        'iat': dt.datetime.utcnow(),
        'identity': user_id
    }
    return jwt.encode(payload, secret, algorithm)


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and verify_password(password, user.hashed_password, user.salt):
        return user
    return None


def identity(payload):
    id = payload.get('identity')
    return UserModel.query.get(id)


def jwt_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')
        if not jwt_token:
            return jsonify({'message': 'Unauthenticated'}), 401
        if len(jwt_token.split()) != 2 or not jwt_token.startswith('JWT'):
            return jsonify({'message': 'Wrong token format'}), 401
        access_token = jwt_token.split()[1]
        try:
            payload = jwt.decode(access_token, secret, algorithm)
        except InvalidSignatureError:
            return jsonify({'message': 'Invalid token'}), 401
        if not identity(payload):
            return jsonify({'message': 'Wrong credentials'}), 401
        return f(payload.get('identity'), *args, **kwargs)

    return wrap
