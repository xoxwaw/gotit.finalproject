from main.config import get_env


class BaseEnv:
    DB_USER = get_env('DB_USER')
    DB_PASSWORD = get_env('DB_PASSWORD')
    SECRET_KEY = get_env('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    TESTING = False
