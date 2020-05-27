import datetime as dt
import time
from functools import wraps

import jwt
from flask import request, abort
from jwt.exceptions import InvalidSignatureError

from main.config.base import BaseEnv
from main.constants import UNAUTHENTICATED
from main.models.user import UserModel
from main.controllers.errors import UnAuthenticated

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


def identity(payload):
    user_id = payload.get('identity')
    return UserModel.query.get(user_id)


def jwt_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')
        if not jwt_token:
            return UnAuthenticated(message='Empty token').to_json()
        if len(jwt_token.split()) != 2 or not jwt_token.startswith('JWT'):
            return UnAuthenticated(message='Wrong token format').to_json()
        access_token = jwt_token.split()[1]
        payload = None
        try:
            payload = jwt.decode(access_token, secret, algorithm)
        except InvalidSignatureError:
            return UnAuthenticated(message='Invalid token').to_json()
        if not identity(payload):
            return UnAuthenticated(message='Wrong credentials').to_json()
        if payload.get('exp') < time.time():
            return UnAuthenticated(message='Token expired').to_json()
        return f(payload.get('identity'), *args, **kwargs)

    return wrap
