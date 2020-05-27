from flask import jsonify, Response


class BaseException(Response):
    status_code = 500
    message = ''

    def to_json(self):
        return jsonify({'message': self.message}), self.status_code


class BadRequest(BaseException):
    def __init__(self, message='Bad Request'):
        super(BadRequest, self).__init__()
        self.status_code = 400
        self.message = message


class UnAuthenticated(BaseException):
    def __init__(self, message='Unauthenticated'):
        super(UnAuthenticated, self).__init__()
        self.status_code = 401
        self.message = message


class Forbidden(BaseException):
    def __init__(self, message='Forbidden'):
        super(Forbidden, self).__init__()
        self.status_code = 403
        self.message = message


class NotFound(BaseException):
    def __init__(self, message='Not Found'):
        super(NotFound, self).__init__()
        self.status_code = 404
        self.message = message
