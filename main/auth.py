import datetime as dt
import time
from functools import wraps

import jwt
from flask import request, abort
from jwt.exceptions import InvalidSignatureError

from main.config import conf
from main.models.user import UserModel

algorithm = 'HS256'
secret = conf.SECRET_KEY


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
            abort(401, {'message': 'Empty token'})
        jwt_comps = jwt_token.split(' ')
        if len(jwt_comps) != 2 or not jwt_token.startswith('JWT'):
            abort(401, {'message': 'Wrong token format'}).to_json()
        access_token = jwt_comps[1]
        try:
            payload = jwt.decode(access_token, secret, algorithm)
        except InvalidSignatureError:
            abort(401, {'message': 'Invalid token'})
        if identity(payload) is None:
            abort(401, {'message': 'Wrong credentials'})
        if payload.get('exp') < time.time():
            abort(401, {'message': 'Token expired'})
        return f(payload.get('identity'), *args, **kwargs)

    return wrap
