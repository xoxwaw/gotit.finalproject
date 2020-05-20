import pytest

from main.db import db
from tests.helper import login


def test_register(client, app):
    client.post('/register', data={
        'username': 'user_test', 'password': 'password'})
    with app.app_context():
        assert db.engine.execute(
            "SELECT * FROM users WHERE username='user_test'"
        ).fetchone() is not None


def test_auth(client, app):
    data = login(client, 'user_test', 'password')
    assert data.get('access_token', "").count('.') == 2

