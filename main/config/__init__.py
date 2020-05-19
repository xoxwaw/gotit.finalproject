import os

from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

from main.config.dev import DevEnv
from main.config.test import TestEnv


config = None
env = os.getenv('ENV')
if env == 'test':
    config = TestEnv()
else:
    config = DevEnv()


def load(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.secret_key = os.getenv('JWT_SECRET_KEY')
