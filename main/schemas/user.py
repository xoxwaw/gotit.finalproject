from marshmallow import Schema, fields, validate

from main.constants import (
    MAX_USERNAME_LENGTH,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    MIN_USERNAME_LENGTH
)
from main.schemas.helpers import validate_empty_string


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        validate=[
            validate.Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH),
            validate_empty_string
        ])
    password = fields.Str(
        validate=[
            validate.Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH),
            validate_empty_string
        ])


class PasswordSchema(Schema):
    password = fields.Str(validate=[
        validate_empty_string,
        validate.Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH)
])


password_validation_schema = PasswordSchema()
user_schema = UserSchema()
