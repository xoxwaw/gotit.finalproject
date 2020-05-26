from flask import Blueprint, request, jsonify

from main.schemas.user import user_post_validation_schema
from main.models.user import UserModel
from main.libs.password import hash_password, verify_password
from main.auth import encode_jwt
from main.auth import jwt_required
from main.schemas.query import password_validation_schema
from main.controllers.response import (
    PostSuccess, BadRequest, NoContent, Unauthenticated
)


users = Blueprint("users", __name__, url_prefix='/')


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validate = user_post_validation_schema.load(data)
    if len(validate.errors) > 0:
        return BadRequest(errors=validate.errors).__repr__()
    user = UserModel.find_by_username(data.get('username'))
    if user:
        return BadRequest(message= 'user with username {} has already existed'.
                       format(data.get('username'))).__repr__()
    hashed_password, salt = hash_password(data.get('password'))
    user = UserModel(
        username=data.get('username'),
        hashed_password=hashed_password,
        salt=salt,
    )
    user.save_to_db()
    return PostSuccess().__repr__()


@users.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    validate = user_post_validation_schema.load(data)
    if len(validate.errors) > 0:
        return BadRequest(errors=validate.errors).__repr__()
    user = UserModel.find_by_username(data.get('username'))
    if not user:
        return Unauthenticated(message='invalid username or password').__repr__()
    response = {
        'access_token': encode_jwt(user.id).decode()
    }
    return jsonify(response)


@users.route('/password', methods=['PUT'])
@jwt_required
def password(user_id):
    user = UserModel.query.get(user_id)
    data = request.get_json()
    if not verify_password(data.get('old_password'), user.hashed_password, user.salt):
        return BadRequest(message='Wrong password').__repr__()
    validate = password_validation_schema.load(data.get('new_password'))
    if len(validate.errors) > 0:
        return BadRequest(errors=validate.errors).__repr__()
    hashed_password, salt = hash_password(data.get('new_password'))
    user.hashed_password = hashed_password
    user.salt = salt
    user.save_to_db()
    return NoContent().__repr__()
