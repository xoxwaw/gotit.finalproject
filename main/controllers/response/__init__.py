from flask import jsonify


class Response:
    def __init__(self, message, errors=None):
        self.status_code = 200
        self.message = message
        self.errors = errors

    def __repr__(self):
        if self.errors is not None:
            return jsonify({'message': self.message, 'errors': self.errors}), self.status_code
        return jsonify({'message': self.message}), self.status_code


class PostSuccess(Response):
    def __init__(self, message='OK'):
        super(PostSuccess, self).__init__(message)
        self.status_code = 201


class NoContent:

    status_code = 204

    def __repr__(self):
        return '', self.status_code


class BadRequest(Response):
    def __init__(self, message='Bad Request', errors=None):
        super(BadRequest, self).__init__(message, errors)
        self.status_code = 400


class Unauthenticated(Response):
    def __init__(self, message='Unauthenticated', errors=None):
        super(Unauthenticated, self).__init__(message, errors)
        self.status_code = 401


class Unauthorized(Response):
    def __init__(self, message='Unauthorized', errors=None):
        super(Unauthorized, self).__init__(message, errors)
        self.status_code = 403


class NotFound(Response):
    def __init__(self, message='Not found', errors=None):
        super(NotFound, self).__init__(message, errors)
        self.status_code = 404