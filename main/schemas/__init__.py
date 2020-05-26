from marshmallow import Schema, fields, validate

from main.constants import ITEM_NAME_LENGTH


class QuerySchema(Schema):
    name = fields.Str(validate=validate.Length(min=6, max=ITEM_NAME_LENGTH), allow_none=True)
    page = fields.Integer(allow_none=True, validate=validate.Range(min=1), default=1)
    per_page = fields.Integer(allow_none=True, validate=validate.Range(min=1), default=10)
    category_id = fields.Integer(allow_none=True, validate=validate.Range(min=1))


query_validation_schema = QuerySchema()
