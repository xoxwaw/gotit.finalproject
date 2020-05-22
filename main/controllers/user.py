from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from main.schemas.validations.user import user_validation_schema
from main.models.user import UserModel
from main.libs.password import encoder, verify_password
from main.auth import encode_jwt
from main.auth import jwt_required

users = Blueprint("users", __name__, url_prefix='/')


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_validation_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = UserModel.find_by_username(data.get('username'))
    if user:
        return jsonify({'message': 'user with username {} has already existed'.
                       format(data.get('username'))}), 400
    hashed_password, salt = encoder(data.get('password'))
    user = UserModel(
        username=data.get('username'),
        hashed_password=hashed_password,
        salt=salt,
    )
    UserModel.save_to_db(user)
    return jsonify({'message': 'OK'}), 201


@users.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    try:
        user_validation_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = UserModel.find_by_username(data.get('username'))
    if not user:
        return jsonify({'message': 'invalid username or password'}), 401
    response = {
        'access_token': encode_jwt(user.id).decode()
    }
    return jsonify(response), 200


@users.route('/password', methods=['PUT'])
@jwt_required
def password(id):
    user = UserModel.query.get(id)
    data = request.get_json()
    if not verify_password(user.hashed_password, user.salt, data.get('old_password')):
        return jsonify({'message': 'Wrong password'}), 400
    hashed_password, salt = encoder(data.get('new_password'))
    user.hashed_password = hashed_password
    user.salt = salt
    UserModel.save_to_db(user)
    return '', 204
