from marshmallow import Schema, fields, validate


class ItemValidationSchema(Schema):
    name = fields.Str(validate=validate.Length(min=6, max=128), allow_none=True)
    page = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)
    category_id = fields.Integer(allow_none=True)


item_validation_schema = ItemValidationSchema()
