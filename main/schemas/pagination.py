from marshmallow import Schema, fields, validate

from main.constants import ITEM_NAME_LENGTH, MIN_ITEM_NAME_LENGTH


class PaginationSchema(Schema):
    name = fields.Str(validate=validate.Length(min=MIN_ITEM_NAME_LENGTH, max=ITEM_NAME_LENGTH), allow_none=True)
    page = fields.Integer(allow_none=True, validate=validate.Range(min=1), default=1)
    per_page = fields.Integer(allow_none=True, validate=validate.Range(min=1, max=50), default=10)


class ItemPaginationSchema(PaginationSchema):
    category_id = fields.Integer(allow_none=True, validate=validate.Range(min=1))


pagination_schema = PaginationSchema()
item_pagination_schema = ItemPaginationSchema()
