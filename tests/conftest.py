import pytest

from main import create_app
from main.db import db
from tests import populate_data


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        populate_data()
    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()
