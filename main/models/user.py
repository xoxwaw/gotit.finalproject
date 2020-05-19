from main.db import db, ma
from main.constants import USERNAME_LEN, HASHED_PASSWORD_LEN, SALT_LEN
from main.models.db_action_mixin import DBActionMixin


class UserModel(db.Model, DBActionMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_LEN), unique=True)
    hashed_password = db.Column(db.String(HASHED_PASSWORD_LEN))
    salt = db.Column(db.String(SALT_LEN))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')


user_schema = UserSchema(strict=True)
