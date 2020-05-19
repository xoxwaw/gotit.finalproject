from flask import Blueprint

from main.models.user import UserModel


users = Blueprint('users', __name__, url_prefix='/')


@users.route('/register', methods=['POST'])
def register():

    return {'message': 'OK'}, 201


@users.route('/auth', methods=['POST'])
def auth():
    pass


@users.route('/password', methods=['PUT'])
def password():
    pass
