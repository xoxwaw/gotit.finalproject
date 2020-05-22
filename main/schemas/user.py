from datetime import datetime as dt

from marshmallow import Schema, fields, validate, post_load

from main.models.user import UserModel


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(validate=validate.Length(min=6, max=30))
    password = fields.Str(load_only=True)

    @post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        return UserModel(
            username=data['username'],
            hashed_password=data['hashed_password'],
            salt=data['salt'],
        )


user_schema = UserSchema()
