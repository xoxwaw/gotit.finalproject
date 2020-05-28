from main.constants import ITEM_NAME_LENGTH, MAX_DESC_LENGTH
from main.db import db
from main.models.base_model import BaseModel


class ItemModel(db.Model, BaseModel):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(ITEM_NAME_LENGTH), nullable=False)
    description = db.Column(db.String(MAX_DESC_LENGTH))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    category = db.relationship('CategoryModel', lazy='joined')
    user = db.relationship('UserModel', lazy='joined')

    def __init__(self, **kwargs):
        super(ItemModel, self).__init__(**kwargs)
