from main.db import db
from tests import TEST_UNAUTH_USER, TEST_PASSWORD, TEST_USERNAME
from tests.helpers import (
    login,
    post_category,
    delete_category,
    update_category,
)


def test_post_category(client, app):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {'name': 'test_category', 'description': 'This is a very nice category.'}
    status_code = post_category(client, access_token, data)
    assert status_code == 200


def test_update_category(client, app):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 'modified_name'
    }
    id = 1
    status_code = update_category(client, access_token, id, data)
    assert status_code == 204


def test_delete_category(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = delete_category(client, access_token, 1)
    assert status_code == 204


def test_unauthorized_access_delete_category(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    status_code = delete_category(client, access_token, 3)
    assert status_code == 403


def test_unauthorized_access_update_category(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 'modified_name',
    }
    id = 8
    status_code = update_category(client, access_token, id, data)
    assert status_code == 403


def test_invalid_format_post_category(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 0
    }
    status_code = post_category(client, access_token, data)
    assert status_code == 400


def test_get_categories(client):
    response = client.get('/categories/')
    assert response.status_code == 200


def test_blank_name_categories(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': '         ',
        'description': 'filled with spaces'
    }
    status_code = post_category(client, access_token, data)
    assert status_code == 400
