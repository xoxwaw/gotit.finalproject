import logging
import os
from importlib import import_module

from dotenv import load_dotenv
from flask import Flask

load_dotenv('envs/{}/.env'.format(os.getenv('ENV')))

from main.controllers.category import categories
from main.controllers.item import items
from main.controllers.user import users
from main.db import db


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)


def create_app(env):
    app = Flask(__name__)
    module = None
    try:
        module = import_module('main.config.{}'.format(env))
    except ModuleNotFoundError:
        logging.error('Environment {} not found'.format(env))
        exit(1)
    Config = getattr(module, 'Config')
    app.config.from_object(Config())
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(items, url_prefix='/items')
    app.register_blueprint(categories, url_prefix='/categories')
    return app
