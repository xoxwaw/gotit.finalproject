from functools import wraps

from flask import jsonify, Response, request


class BaseException(Response):
    status_code = 500
    message = ''
    errors = None

    def to_json(self):
        if self.errors is not None:
            jsonify({'message': self.message, 'errors': self.errors}), self.status_code
        return jsonify({'message': self.message}), self.status_code


class BadRequest(BaseException):
    def __init__(self, message='Bad Request', errors=None):
        super(BadRequest, self).__init__()
        self.status_code = 400
        self.message = message
        self.errors = errors


class UnAuthenticated(BaseException):
    def __init__(self, message='Unauthenticated', errors=None):
        super(UnAuthenticated, self).__init__()
        self.status_code = 401
        self.message = message
        self.errors = errors


class Forbidden(BaseException):
    def __init__(self, message='Forbidden', errors=None):
        super(Forbidden, self).__init__()
        self.status_code = 403
        self.message = message
        self.errors = errors


class NotFound(BaseException):
    def __init__(self, message='Not Found', errors=None):
        super(NotFound, self).__init__()
        self.status_code = 404
        self.message = message
        self.errors = errors


def validate_get_input(schema):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            data = schema.load(request.args)
            validate = schema.load(data)
            if len(validate.errors) > 0:
                return BadRequest(errors=validate.errors).to_json()
            return func(validate, *args, **kwargs)

        return inner

    return decorator


def validate_post_input(schema):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            data = schema.load(request.get_json())
            validate = schema.load(data)
            if len(validate.errors) > 0:
                import sys
                print(validate.errors, file=sys.stderr)
                return BadRequest(errors=validate.errors).to_json()
            return func(validate, *args, **kwargs)

        return inner

    return wrapper
