from flask import Flask

import main.config as cfg
from main.controllers.user import users
from main.controllers.item import items
from main.controllers.category import categories


def create_app():
    app = Flask(__name__)
    cfg.load(app)
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(items, url_prefix='/items')
    app.register_blueprint(categories, url_prefix='/categories')
    return app
