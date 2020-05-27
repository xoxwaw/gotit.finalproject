from flask import Blueprint, jsonify

from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__, url_prefix='/')


@errors.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify({'message': e.description['message']}), code
