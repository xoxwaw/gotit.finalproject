from main.db import db
from main.constants import ITEM_NAME_LEN
from main.models.db_action_mixin import DBActionMixin


class ItemModel(db.Model, DBActionMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(ITEM_NAME_LEN))
    description = db.Column(db.Text())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    store = db.relationship('CategoryModel')
    user = db.relationship('UserModel')

    def __init__(self, **kwargs):
        super(ItemModel, self).__init__(**kwargs)
