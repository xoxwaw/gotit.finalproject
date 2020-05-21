from datetime import datetime as dt
import sys

from marshmallow import Schema, fields, validate, post_load, post_dump
from main.schema.user import UserSchema
from main.schema.category import CategorySchema
from main.models.item import ItemModel


class ItemDescriptionSchema(Schema):
    image_url = fields.URL()
    price = fields.Float()
    description = fields.Str()

class ItemOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(ItemDescriptionSchema)
    category_id = fields.Nested(CategorySchema, only=('id', 'name'))
    creator_id = fields.Nested(UserSchema, only=('id', 'username'))
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class ItemInputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(ItemDescriptionSchema)
    category_id = fields.Integer()
    creator_id = fields.Integer()
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        return ItemModel(
            name=data['name'],
            description=data.get('description'),
            category_id=data.get('category_id'),
            creator_id=data['creator_id'],
            created_at=dt.utcnow(),
            updated_at=dt.utcnow()
        )


item_input_schema = ItemInputSchema()

items_output_schema = ItemOutputSchema(many=True)
item_output_schema = ItemOutputSchema()


