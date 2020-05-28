from main.constants import CATEGORY_NAME_LENGTH, MAX_DESC_LENGTH
from main.db import db
from main.models.base_model import BaseModel


class CategoryModel(db.Model, BaseModel):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(CATEGORY_NAME_LENGTH), nullable=False)
    description = db.Column(db.String(MAX_DESC_LENGTH))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('UserModel', lazy='joined')
    items = db.relationship('ItemModel', lazy='joined')

    def __init__(self, **kwargs):
        super(CategoryModel, self).__init__(**kwargs)
