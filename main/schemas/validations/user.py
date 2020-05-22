from marshmallow import Schema, fields, validate


class UserValidationSchema(Schema):
    username = fields.Str(validate=validate.Length(min=6, max=32), required=True)
    password = fields.Str(validate=validate.Length(min=6, max=128), required=True)


user_validation_schema = UserValidationSchema()
