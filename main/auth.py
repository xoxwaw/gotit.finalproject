import os
import datetime as dt

import jwt

from main.models.user import UserModel
from main.libs.password import verify_password

algorithms = ['HS256']
secret = os.getenv('JWT_SECRET_KEY')

def payload(encoded_jwt):
    """decode a jwt token to payload"""
    payload = jwt.decode(encoded_jwt, secret, algorithms)
    return payload['identity']


def encode_jwt(id):
    """encode payload to a jwt"""
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(days=0, hours=1),
        'iat': dt.datetime.utcnow(),
        'identity': id
    }
    return jwt.encode(payload, secret, algorithms)


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user is not None and verify_password(user.hashed_password, user.salt, password):
        return user
    return None


def identity(payload):
    id = payload['identity']
    return UserModel.find_by_id(id)
