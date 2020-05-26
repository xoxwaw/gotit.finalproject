from main.db import db
from main.constants import USERNAME_LENGTH, HASHED_PASSWORD_LENGTH, SALT_LENGTH
from main.models.db_base_mixin import DBBaseMixin


class UserModel(db.Model, DBBaseMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LENGTH), unique=True)
    hashed_password = db.Column(db.String(HASHED_PASSWORD_LENGTH))
    salt = db.Column(db.String(SALT_LENGTH))

    category = db.relationship('CategoryModel', lazy='joined', backref='users')
    item = db.relationship('ItemModel', lazy='joined', backref='users')

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
