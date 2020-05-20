from datetime import datetime as dt

from marshmallow import Schema, fields, validate, post_load

from main.schema.user import UserSchema
from main.models.category import CategoryModel


class CategoryDescriptionSchema(Schema):
    image_url = fields.URL()
    description = fields.String()


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    creator= fields.Nested(UserSchema, only=('id', 'username'), dump_only=True)
    created_at = fields.DateTime(required=True, dump_only=True)
    updated_at = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        return CategoryModel(
            name=data['name'],
            description=data.get('description', None),
            creator_id=data['creator_id'],
            created_at=dt.utcnow(),
            updated_at=dt.utcnow()
        )

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)