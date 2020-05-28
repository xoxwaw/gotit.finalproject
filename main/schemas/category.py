from marshmallow import Schema, fields, validate

from main.constants import CATEGORY_NAME_LENGTH, MAX_DESC_LENGTH, MIN_CATEGORY_NAME_LENGTH
from main.schemas.helpers import validate_empty_string
from main.schemas.user import UserSchema


class CategoryOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    user = fields.Nested(UserSchema, only=('id', 'username'))


class CategoryInputSchema(Schema):
    name = fields.Str(
        validate=[
            validate.Length(min=MIN_CATEGORY_NAME_LENGTH, max=CATEGORY_NAME_LENGTH),
            validate_empty_string
        ], required=True)
    description = fields.Str(validate=validate.Length(max=MAX_DESC_LENGTH))


category_input_schema = CategoryInputSchema()
category_output_schema = CategoryOutputSchema()
categories_output_schema = CategoryOutputSchema(many=True)
