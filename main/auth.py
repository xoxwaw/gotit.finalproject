import datetime as dt
import sys
import time
from functools import wraps

import jwt
from flask import request, abort
from jwt.exceptions import InvalidSignatureError

from main.config.base import BaseEnv
from main.constants import UNAUTHENTICATED
from main.libs.password import verify_password
from main.models.user import UserModel

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
    user_id = payload.get('identity')
    return UserModel.query.get(user_id)


def jwt_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')
        if not jwt_token:
            abort(UNAUTHENTICATED, 'Invalid token')
        if len(jwt_token.split()) != 2 or not jwt_token.startswith('JWT'):
            abort(UNAUTHENTICATED, 'Wrong token format')
        access_token = jwt_token.split()[1]
        payload = None
        try:
            payload = jwt.decode(access_token, secret, algorithm)
            print(payload, time.time(), file=sys.stderr)
        except InvalidSignatureError:
            abort(UNAUTHENTICATED, 'Invalid token')
        if not identity(payload):
            abort(UNAUTHENTICATED, 'Wrong credentials')
        if payload.get('exp') < time.time():
            abort(UNAUTHENTICATED, 'Token expired')
        return f(payload.get('identity'), *args, **kwargs)

    return wrap
