import json

from main.db import db
from tests import TEST_USERNAME, TEST_PASSWORD, TEST_UNAUTH_USER
from tests.helpers import login, post_category


def test_register(client, app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/register', data=json.dumps({
        'username': TEST_UNAUTH_USER, 'password': TEST_PASSWORD
    }), headers=headers)
    with app.app_context():
        assert db.engine.execute(
            "SELECT * FROM users WHERE username='user_test'"
        ).fetchone() is not None


def test_auth(client, app):
    token = login(client, TEST_USERNAME, TEST_PASSWORD)
    assert token.count('.') == 2


def test_wrong_token_format(client, app):
    data = {'name': 'phone book'}
    status_code = post_category(client, "", data)
    assert status_code == 400


def test_incorrect_access_token(client, app):
    data = {'name': 'phone book'}
    token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = post_category(client, token + 'a', data)
    assert status_code == 401
