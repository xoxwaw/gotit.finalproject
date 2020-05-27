from main.db import db
from tests import TEST_UNAUTH_USER, TEST_PASSWORD, TEST_USERNAME
from tests.helpers import (
    login,
    post_category,
    delete_category,
    update_category,
)


def test_post_category(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {'name': 'test_category', 'description': 'This is a very nice category.'}
    status_code = post_category(client, access_token, data)
    assert status_code == 200
    with app.app_context():
        assert db.session.execute(
            'SELECT * FROM categories WHERE name="test_category"'
        ).fetchone() is not None


def test_update_category(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 'modified_name'
    }
    id = 1
    status_code = update_category(client, access_token, id, data)
    assert status_code == 204
    with app.app_context():
        category = db.session.execute(
            'SELECT * FROM categories WHERE id={}'.format(id)
        ).fetchone()
        assert category.name == 'modified_name'


def test_delete_category(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = delete_category(client, access_token, 1)
    assert status_code == 204


def test_unauthorized_access_delete_category(client, app):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    status_code = delete_category(client, access_token, 3)
    assert status_code == 403


def test_unauthorized_access_update_category(client, app):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 'modified_name',
    }
    id = 8
    status_code = update_category(client, access_token, id, data)
    assert status_code == 403


def test_invalid_format_post_category(client, app):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 0
    }
    status_code = post_category(client, access_token, data)
    assert status_code == 400
