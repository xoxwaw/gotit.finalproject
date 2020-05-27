from main.constants import CATEGORY_NAME_LENGTH, MAX_DESC_LENGTH
from main.db import db
from main.models.db_base_mixin import DBBaseMixin


class CategoryModel(db.Model, DBBaseMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(CATEGORY_NAME_LENGTH), nullable=False)
    description = db.Column(db.String(MAX_DESC_LENGTH))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('UserModel', lazy='joined')
    items = db.relationship('ItemModel', lazy='joined')

    def __init__(self, **kwargs):
        super(CategoryModel, self).__init__(**kwargs)
