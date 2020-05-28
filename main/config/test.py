from main.config import get_env
from main.config.base import BaseEnv


class Config(BaseEnv):
    DB_NAME = get_env('TEST_DB_NAME')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(
        BaseEnv.DB_USER, BaseEnv.DB_PASSWORD, DB_NAME)
    TESTING = True
