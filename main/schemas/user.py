from marshmallow import Schema, fields, validate

from main.constants import (
    MAX_USERNAME_LENGTH,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    MIN_USERNAME_LENGTH
)
from main.schemas import validate_white_spaces


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(validate=validate.Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH))
    password = fields.Str(load_only=True, validate=validate.Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH))


class UserPostValidationSchema(Schema):
    username = fields.Str(
        validate=[
            validate.Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH),
            validate_white_spaces
        ])
    password = fields.Str(
        validate=[
            validate.Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH),
            validate_white_spaces
        ])


user_schema = UserSchema()
user_post_validation_schema = UserPostValidationSchema()
