from main.db import db
from main.constants import MAX_USERNAME_LENGTH, HASHED_PASSWORD_LENGTH, SALT_LENGTH
from main.models.db_base_mixin import DBBaseMixin


class UserModel(db.Model, DBBaseMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH), unique=True)
    hashed_password = db.Column(db.String(HASHED_PASSWORD_LENGTH), nullable=False)
    salt = db.Column(db.String(SALT_LENGTH), nullable=False)

    category = db.relationship('CategoryModel', lazy='joined')
    item = db.relationship('ItemModel', lazy='joined')

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
