from marshmallow import Schema, fields, validate

from main.constants import ITEM_NAME_LENGTH, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
from main.schemas import validate_white_spaces

MIN_ITEM_NAME_LENGTH = 3


class QuerySchema(Schema):
    name = fields.Str(validate=validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH), allow_none=True)
    page = fields.Integer(allow_none=True, validate=validate.Range(min=1), default=1)
    per_page = fields.Integer(allow_none=True, validate=validate.Range(min=1), default=10)
    category_id = fields.Integer(allow_none=True, validate=validate.Range(min=1))


class PasswordSchema(Schema):
    password = fields.Str(validate=[
        validate_white_spaces,
        validate.Length(min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH)
    ])


query_validation_schema = QuerySchema()
password_validation_schema = PasswordSchema()
