from marshmallow import Schema, fields, validate


class CategoryValidationSchema(Schema):
    name = fields.Str(validate=validate.Length(min=6, max=128), allow_none=True)
    page = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)


category_validation_schema = CategoryValidationSchema()
