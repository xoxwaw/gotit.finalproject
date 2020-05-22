from marshmallow import Schema, fields, validate

from main.schemas.user import UserSchema


class CategoryDescriptionSchema(Schema):
    image_url = fields.URL()
    description = fields.String()


class CategoryOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    user= fields.Nested(UserSchema, only=('id', 'username'))


class CategoryInputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=validate.Length(min=3, max=128), required=True)
    description = fields.Nested(CategoryDescriptionSchema)
    creator= fields.Integer()


category_input_schema = CategoryInputSchema()
category_output_schema = CategoryOutputSchema()
categories_output_schema = CategoryOutputSchema(many=True)