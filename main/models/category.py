from main.db import db, ma
from main.models.db_action_mixin import DBActionMixin
from main.constants import CATEGORY_NAME_LEN


class CategoryModel(db.Model, DBActionMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(CATEGORY_NAME_LEN))
    description = db.Column(db.Text())
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('UserModel')
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, **kwargs):
        super(CategoryModel, self).__init__(**kwargs)


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


category_schema = CategorySchema(strict=True)
categories_schema = CategorySchema(strict=True, many=True)
