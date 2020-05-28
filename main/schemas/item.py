from marshmallow import Schema, fields, validate

from main.constants import ITEM_NAME_LENGTH, MAX_DESC_LENGTH, MIN_ITEM_NAME_LENGTH
from main.schemas.category import CategoryInputSchema
from main.schemas.helpers import validate_empty_string
from main.schemas.user import UserSchema


class ItemOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    category = fields.Nested(CategoryInputSchema, only=('id', 'name', 'description'))
    user = fields.Nested(UserSchema)


class ItemInputSchema(Schema):
    name = fields.Str(
        validate=[
            validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH),
            validate_empty_string
        ], required=True)
    description = fields.Str(validate=validate.Length(max=MAX_DESC_LENGTH))
    category_id = fields.Int(validate=validate.Range(min=1))


item_input_schema = ItemInputSchema()

items_output_schema = ItemOutputSchema(many=True)
item_output_schema = ItemOutputSchema()
