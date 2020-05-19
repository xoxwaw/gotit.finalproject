from flask import Flask

import main.config as cfg
from main.controllers.user import users
from main.controllers.item import items
from main.controllers.category import categories
from main.db import db


app = Flask(__name__)
cfg.load(app)
app.register_blueprint(users, url_prefix='/')
app.register_blueprint(items, url_prefix='/items')
app.register_blueprint(categories, url_prefix='/categories')


@app.before_first_request
def create_table():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8000, debug=True)
