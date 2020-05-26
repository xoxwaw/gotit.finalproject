from main.config import validate_env


class BaseEnv:
    DB_USER = validate_env('DB_USER')
    DB_PASSWORD = validate_env('DB_PASSWORD')
    SECRET_KEY = validate_env('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False