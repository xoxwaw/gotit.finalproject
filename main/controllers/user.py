from flask import Blueprint, request, jsonify, abort

from main.auth import encode_jwt
from main.auth import jwt_required
from main.libs.password import hash_password, verify_password
from main.models.user import UserModel
from main.schemas.user import user_schema, password_validation_schema

users = Blueprint("users", __name__, url_prefix='/')  # /users


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validate = user_schema.load(data)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors}).to_json()
    user = UserModel.find_by_username(data.get('username'))
    if user is not None:
        abort(400, {'message': 'user with username {} has already existed'.
              format(data.get('username'))})
    hashed_password, salt = hash_password(data.get('password'))
    user = UserModel(
        username=data.get('username'),
        hashed_password=hashed_password,
        salt=salt,
    )
    user.save_to_db()
    return '', 204


@users.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    validate = user_schema.load(data)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors}).to_json()
    user = UserModel.find_by_username(data.get('username'))
    if user is None:
        abort(401, {'message': 'invalid username or password'}).to_json()
    response = {
        'access_token': encode_jwt(user.id).decode('UTF-8')
    }
    return jsonify(response)


@users.route('/password', methods=['PUT'])
@jwt_required
def password(user_id):
    user = UserModel.query.get(user_id)
    data = request.get_json()
    if not verify_password(data.get('old_password'), user.hashed_password, user.salt):
        abort(401, {'message': 'Wrong password'}).to_json()
    validate = password_validation_schema.load({'password': data.get('new_password')})
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors}).to_json()
    hashed_password, salt = hash_password(data.get('new_password'))
    user.hashed_password = hashed_password
    user.salt = salt
    user.save_to_db()
    return '', 204
