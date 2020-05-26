import sys
import datetime as dt
import time
from functools import wraps

import jwt
from jwt.exceptions import InvalidSignatureError
from flask import request

from main.config.base import BaseEnv
from main.models.user import UserModel
from main.libs.password import verify_password
from main.controllers.response import Unauthenticated


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
            return Unauthenticated().__repr__()
        if len(jwt_token.split()) != 2 or not jwt_token.startswith('JWT'):
            return Unauthenticated(message='Wrong token format').__repr__()
        access_token = jwt_token.split()[1]
        try:
            payload = jwt.decode(access_token, secret, algorithm)
            print(payload, time.time(), file=sys.stderr)
        except InvalidSignatureError:
            return Unauthenticated(message='Invalid token').__repr__()
        if not identity(payload):
            return Unauthenticated(message='Wrong credentials').__repr__()
        if payload.get('exp') < time.time():
            return Unauthenticated(message='Token expired').__repr__()
        return f(payload.get('identity'), *args, **kwargs)

    return wrap
