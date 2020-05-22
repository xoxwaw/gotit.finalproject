from datetime import datetime as dt

from marshmallow import Schema, fields, validate, post_load, pre_load

from main.schema.user import UserSchema
from main.models.category import CategoryModel


class CategoryDescriptionSchema(Schema):
    image_url = fields.URL()
    description = fields.String()


class CategoryOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    creator= fields.Nested(UserSchema, only=('id', 'username'))
    created_at = fields.DateTime( dump_only=True)
    updated_at = fields.DateTime( dump_only=True)

    @post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        return CategoryModel(
            name=data['name'],
            description=data.get('description', None),
            creator_id=data.get('creator_id'),
        )


class CategoryInputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    creator= fields.Integer()
    created_at = fields.DateTime( dump_only=True)
    updated_at = fields.DateTime( dump_only=True)


category_input_schema = CategoryInputSchema()
category_output_schema = CategoryOutputSchema()
categories_output_schema = CategoryOutputSchema(many=True)