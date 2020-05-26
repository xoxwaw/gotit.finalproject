from marshmallow import Schema, fields, validate

from main.constants import USERNAME_LENGTH, PASSWORD_LENGTH


MIN_USERNAME_LENGTH = 6
MIN_PASSWORD_LENGTH = 6


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(validate=validate.Length(min=MIN_USERNAME_LENGTH, max=USERNAME_LENGTH))
    password = fields.Str(load_only=True, validate=validate.Length(min=MIN_PASSWORD_LENGTH, max=PASSWORD_LENGTH))


class UserPostValidationSchema(Schema):
    username = fields.Str(validate=validate.Length(min=MIN_USERNAME_LENGTH, max=USERNAME_LENGTH))
    password = fields.Str(validate=validate.Length(min=MIN_PASSWORD_LENGTH, max=PASSWORD_LENGTH))


user_schema = UserSchema()
user_post_validation_schema = UserPostValidationSchema()
