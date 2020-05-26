from marshmallow import Schema, fields, validate

from main.schemas.user import UserSchema
from main.constants import ITEM_NAME_LENGTH
from main.schemas.category import CategoryInputSchema


MIN_ITEM_NAME_LENGTH = 3

class ItemDescriptionSchema(Schema):
    image_url = fields.URL()
    price = fields.Float()
    description = fields.Str()


class ItemOutputSchema(Schema):
    id = fields.Int()
    name = fields.Str(validate=validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH), required=True)
    description = fields.Nested(ItemDescriptionSchema)
    category = fields.Nested(CategoryInputSchema, only=('id', 'name', 'description'))
    user = fields.Nested(UserSchema)


class ItemInputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH), required=True)
    description = fields.Nested(ItemDescriptionSchema)
    category_id = fields.Integer()
    creator_id = fields.Integer()


item_input_schema = ItemInputSchema()

items_output_schema = ItemOutputSchema(many=True)
item_output_schema = ItemOutputSchema()
