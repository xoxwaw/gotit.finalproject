from main.db import db
from main.constants import ITEM_NAME_LENGTH, MAX_DESC_LENGTH
from main.models.db_base_mixin import DBBaseMixin


class ItemModel(db.Model, DBBaseMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(ITEM_NAME_LENGTH), nullable=False)
    description = db.Column(db.String(MAX_DESC_LENGTH))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    category = db.relationship('CategoryModel', lazy='joined')
    creator = db.relationship('UserModel', lazy='joined')

    def __init__(self, **kwargs):
        super(ItemModel, self).__init__(**kwargs)
