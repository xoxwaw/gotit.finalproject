import datetime as dt
import time
from functools import wraps
from importlib import import_module
import os

import jwt
from flask import request
from jwt.exceptions import InvalidSignatureError

from main.controllers.errors import UnAuthenticated
from main.models.user import UserModel

algorithm = 'HS256'

module = import_module('main.config.{}'.format(os.getenv('ENV')))
Config = getattr(module, 'Config')
secret = Config().SECRET_KEY


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
        if jwt_token is None:
            return UnAuthenticated(message='Empty token').to_json()
        if len(jwt_token.split(' ')) != 2 or not jwt_token.startswith('JWT'):
            return UnAuthenticated(message='Wrong token format').to_json()
        access_token = jwt_token.split(' ')[1]
        try:
            payload = jwt.decode(access_token, secret, algorithm)
        except InvalidSignatureError:
            return UnAuthenticated(message='Invalid token').to_json()
        if identity(payload) is None:
            return UnAuthenticated(message='Wrong credentials').to_json()
        if payload.get('exp') < time.time():
            return UnAuthenticated(message='Token expired').to_json()
        return f(payload.get('identity'), *args, **kwargs)

    return wrap
