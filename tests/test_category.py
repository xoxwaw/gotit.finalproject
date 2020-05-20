import pytest

from main.db import db
from tests.helper import login, post_category, TEST_USERNAME, TEST_PASSWORD


def test_create(client, app):
    data = login(client, TEST_USERNAME, TEST_PASSWORD)
    access_token = data.get('access_token', '')
    assert access_token.count('.') == 2
    data = {'name': 'test_category', 'creator_id': 1}
    status_code = post_category(client, access_token, data)
    assert status_code == 201
    with app.app_context():
        assert db.session.execute(
            'SELECT * FROM categories WHERE name="test_category"'
        ).fetchone() is not None


