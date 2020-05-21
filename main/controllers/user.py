from datetime import datetime as dt
import sys

from flask import Blueprint, request, jsonify

from main.schema.user import user_schema
from main.models.user import UserModel
from main.libs.password import encoder
from main.auth import encode_jwt


users = Blueprint("users", __name__, url_prefix='/')


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = UserModel.find_by_username(data.get('username'))
    if user:
        return jsonify({'message': 'user with username {} has already existed'.
                       format(data.get('username'))}), 400
    hashed_password, salt = encoder(data.get('password'))
    user = UserModel(
        username=data.get('username'),
        hashed_password=hashed_password,
        salt=salt,
        created_at=dt.utcnow(),
        updated_at=dt.utcnow()
    )
    UserModel.save_to_db(user)
    return jsonify({'message': 'OK'}), 201


@users.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    user = UserModel.find_by_username(data.get('username'))
    if not user:
        return jsonify({'message': 'invalid username or password'}), 401
    response = {
        'message': 'ok',
        'access_token': encode_jwt(user.id).decode()
    }
    return jsonify(response), 200


@users.route('/password', methods=['PUT'])
def password():
    pass
