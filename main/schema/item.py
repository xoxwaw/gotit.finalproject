from datetime import datetime as dt

from marshmallow import Schema, fields, validate, post_load
from main.schema.user import UserSchema
from main.schema.category import CategorySchema
from main.models.item import ItemModel


class ItemDescriptionSchema(Schema):
    image_url = fields.URL
    price = fields.Float
    description = fields.Str()

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(ItemDescriptionSchema)
    category = fields.Nested(CategorySchema, only=('id', 'name'))
    creator = fields.Nested(UserSchema, only=('id', 'username'), dump_only=True)
    created_at = fields.DateTime(required=True, dump_only=True)
    updated_at = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        return ItemModel(
            name=data['name'],
            description=data.get('description', ""),
            category_id=data.get('category_id', None),
            creator_id=data['creator_id'],
            created_at=dt.utcnow(),
            updated_at=dt.utcnow()
        )

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)



