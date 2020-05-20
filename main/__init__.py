from flask import Flask

import main.config as cfg
from main.controllers.user import users
from main.controllers.item import items
from main.controllers.category import categories


def create_app(env):
    app = Flask(__name__)
    cfg.load(app, env)
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(items, url_prefix='/items')
    app.register_blueprint(categories, url_prefix='/categories')
    return app
