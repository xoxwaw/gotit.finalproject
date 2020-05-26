from flask import Blueprint, request, jsonify

from main.schemas.user import user_schema, user_post_validation_schema
from main.models.user import UserModel
from main.libs.password import hash_password, verify_password
from main.auth import encode_jwt
from main.auth import jwt_required

users = Blueprint("users", __name__, url_prefix='/')


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validate = user_post_validation_schema.load(data)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
    user = UserModel.find_by_username(data.get('username'))
    if user:
        return jsonify({'message': 'user with username {} has already existed'.
                       format(data.get('username'))}), 400
    hashed_password, salt = hash_password(data.get('password'))
    user = UserModel(
        username=data.get('username'),
        hashed_password=hashed_password,
        salt=salt,
    )
    user.save_to_db()
    return jsonify({'message': 'OK'}), 201


@users.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    validate = user_post_validation_schema.load(data)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
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
    if not verify_password(data.get('old_password'), user.hashed_password, user.salt):
        return jsonify({'message': 'Wrong password'}), 400
    hashed_password, salt = hash_password(data.get('new_password'))
    user.hashed_password = hashed_password
    user.salt = salt
    user.save_to_db()
    return '', 204
