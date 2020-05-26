from marshmallow import Schema, fields, validate

from main.schemas.user import UserSchema
from main.constants import ITEM_NAME_LENGTH, MAX_DESC_LENGTH
from main.schemas.category import CategoryInputSchema
from main.schemas import validate_white_spaces


MIN_ITEM_NAME_LENGTH = 3


class ItemOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str(validate=validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH), required=True)
    description = fields.Str(validate=validate.Length(max=MAX_DESC_LENGTH))
    category = fields.Nested(CategoryInputSchema, only=('id', 'name', 'description'))
    creator = fields.Nested(UserSchema)


class ItemInputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        validate=[
            validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH),
            validate_white_spaces
        ], required=True)
    description = fields.Str(validate=validate.Length(max=MAX_DESC_LENGTH))
    category_id = fields.Integer()
    creator_id = fields.Integer()


item_input_schema = ItemInputSchema()

items_output_schema = ItemOutputSchema(many=True)
item_output_schema = ItemOutputSchema()
