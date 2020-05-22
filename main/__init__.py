from flask import Flask

from importlib import import_module

import main.config as cfg
from main.db import db
from main.controllers.user import users
from main.controllers.item import items
from main.controllers.category import categories


def create_app(env):
    app = Flask(__name__)
    module = import_module('main.config.{}'.format(env))
    cfg_obj = getattr(module, 'Config')
    app.config.from_object(cfg_obj())
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(items, url_prefix='/items')
    app.register_blueprint(categories, url_prefix='/categories')
    return app
