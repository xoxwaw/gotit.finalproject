from main.config import get_env
from main.config.base import BaseEnv


class Config(BaseEnv):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost/{}'.format(
        BaseEnv.DB_USER, BaseEnv.DB_PASSWORD, BaseEnv.DB_NAME)
