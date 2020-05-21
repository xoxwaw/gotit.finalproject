import os
import datetime as dt
from functools import wraps
import sys

import jwt
from flask import request, jsonify

from main.models.user import UserModel
from main.libs.password import verify_password

algorithm = 'HS256'
secret = os.getenv('JWT_SECRET_KEY')

def get_payload(encoded_jwt):
    """decode a jwt token to payload"""
    payload = jwt.decode(encoded_jwt, secret, algorithm)
    return payload


def encode_jwt(id):
    """encode payload to a jwt"""
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(days=0, hours=1),
        'iat': dt.datetime.utcnow(),
        'identity': id
    }
    return jwt.encode(payload, secret, algorithm)


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and verify_password(user.hashed_password, user.salt, password):
        return user
    return None


def identity(payload):
    id = payload['identity']
    return UserModel.find_by_id(id)


def jwt_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        jwt = request.headers.get('Authorization')
        if not jwt:
            return jsonify({'Unauthenticated'}), 401
        access_token = jwt.split()[1]
        payload = get_payload(access_token)
        if not identity(payload):
            return jsonify({'Wrong credentials'}), 401
        return f(payload.get('identity'), *args, **kwargs)
    return wrap


