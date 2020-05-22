from main.db import db
from main.models.db_action_mixin import DBActionMixin
from main.constants import CATEGORY_NAME_LEN


class CategoryModel(db.Model, DBActionMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(CATEGORY_NAME_LEN))
    description = db.Column(db.Text())
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('UserModel',
                           primaryjoin='and_(CategoryModel.creator_id==UserModel.id)',
                           backref='categories', lazy='joined'
                           )
    items = db.relationship('ItemModel', lazy='joined', backref='categories')

    def __init__(self, **kwargs):
        super(CategoryModel, self).__init__(**kwargs)
