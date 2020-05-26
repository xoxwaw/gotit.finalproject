from main.config.base import BaseEnv
from main.config import validate_env


class Config(BaseEnv):
    DB_NAME = validate_env('DB_NAME')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(
        BaseEnv.DB_USER, BaseEnv.DB_PASSWORD, DB_NAME)
