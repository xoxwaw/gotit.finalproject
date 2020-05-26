from marshmallow import Schema, fields, validate

from main.schemas.user import UserSchema
from main.constants import CATEGORY_NAME_LENGTH
from main.schemas import validate_white_spaces


MIN_CATEGORY_NAME_LENGTH = 3

class CategoryDescriptionSchema(Schema):
    image_url = fields.URL()
    description = fields.Str()


class CategoryOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=MIN_CATEGORY_NAME_LENGTH, max=CATEGORY_NAME_LENGTH), required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    creator = fields.Nested(UserSchema, only=('id', 'username'))


class CategoryInputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        validate=[
            validate.Length(min=MIN_CATEGORY_NAME_LENGTH, max=CATEGORY_NAME_LENGTH),
            validate_white_spaces
        ], required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    creator_id = fields.Int()


category_input_schema = CategoryInputSchema()
category_output_schema = CategoryOutputSchema()
categories_output_schema = CategoryOutputSchema(many=True)
