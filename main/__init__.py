import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

load_dotenv('envs/{}/.env'.format(os.getenv('ENV')))

from main.config import conf
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


def create_app():
    app = Flask(__name__)
    app.config.from_object(conf)
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(items, url_prefix='/items')
    app.register_blueprint(categories, url_prefix='/categories')

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(e.description), code

    return app
