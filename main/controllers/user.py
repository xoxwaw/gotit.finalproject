from datetime import datetime as dt

from flask import Blueprint, request

from main.schema.user import user_schema
from main.models.user import UserModel
from main.libs.password import encoder


users = Blueprint("users", __name__, url_prefix='/')


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = UserModel.find_by_username(data.get('username'))
    if user:
        return {'message': 'user with username {} has already existed'.format}
    user = UserModel(
        username=data.get('username'),
        hashed_password=encoder(data.get('password')),
        created_at=dt.utcnow(),
        updated_at=dt.utcnow()
    )
    UserModel.save_to_db(user)
    return {'message': 'OK'}, 201


@users.route('/auth', methods=['POST'])
def auth():
    pass


@users.route('/change_password', methods=['PUT'])
def password():
    pass
