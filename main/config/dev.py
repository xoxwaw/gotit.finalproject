import os

from main.config.base import BaseEnv


class Config(BaseEnv):
    DB_NAME = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(
        BaseEnv.DB_USER, BaseEnv.DB_PASSWORD, DB_NAME)
    TESTING = False
