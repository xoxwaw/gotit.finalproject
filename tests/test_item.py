from main.db import db
from tests.helpers import (
    TEST_PASSWORD,
    TEST_USERNAME,
    login,
    post_item,
    delete_item,
    update_item,
)


def test_post_item(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {'name': 'test_item'}
    status_code = post_item(client, access_token, data)
    assert status_code == 201
    # with app.app_context():
    #     assert db.session.execute(
    #         'SELECT * FROM items WHERE name="test_item"'
    #     ).fetchone() is not None


def test_update_item(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 'modified_name'
    }
    id = 2
    status_code = update_item(client, access_token, id, data)
    assert status_code == 204
    with app.app_context():
        item = db.session.execute(
            'SELECT * FROM items WHERE id={}'.format(id)
        ).fetchone()
        assert item.name == 'modified_name'


def test_delete_item(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = delete_item(client, access_token, 6)
    assert status_code == 204
