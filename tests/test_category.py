from main.db import db
from tests.helpers import (
    login,
    post_category,
    delete_category,
    update_category,
    TEST_USERNAME,
    TEST_PASSWORD
)


def test_post_category(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {'name': 'test_category'}
    status_code = post_category(client, access_token, data)
    assert status_code == 201
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
