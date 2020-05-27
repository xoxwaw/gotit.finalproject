from main.db import db
from tests import TEST_UNAUTH_USER, TEST_USERNAME, TEST_PASSWORD
from tests.helpers import (
    login,
    post_item,
    delete_item,
    update_item,
)


def test_post_item(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {'name': 'test_item'}
    status_code = post_item(client, access_token, data)
    assert status_code == 200


def test_update_item(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 'modified_name'
    }
    id = 2
    status_code = update_item(client, access_token, id, data)
    assert status_code == 204


def test_delete_item(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = delete_item(client, access_token, 6)
    assert status_code == 204


def test_unauthorized_access_delete_item(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    status_code = delete_item(client, access_token, 3)
    assert status_code == 403


def test_unauthorized_access_update_item(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 'modified_name'
    }
    id = 8
    status_code = update_item(client, access_token, id, data)
    assert status_code == 403


def test_unauthorized_assign_category_of_item(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 'invalid item',
        'category_id': 4
    }
    status_code = post_item(client, access_token, data)
    assert status_code == 403


def test_post_invalid_format_category(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 'new category',
        'category_id': 'hello'
    }
    status_code = post_item(client, access_token, data)
    assert status_code == 400


def test_get_items(client):
    response = client.get('/items/')
    assert response.status_code == 200


def test_get_nonexistent_item(client):
    response = client.get('/items/100')
    assert response.status_code == 404


def test_wrong_format_update_item(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 0,
        'category_id': 2
    }
    status_code = update_item(client, access_token, 3, data)
    assert status_code == 400


def test_unauthorized_access_update_category_of_item(client):
    access_token = login(client, TEST_UNAUTH_USER, TEST_PASSWORD)
    data = {
        'name': 'modified_name',
        'category_id': 2
    }
    id = 7
    status_code = update_item(client, access_token, id, data)
    assert status_code == 403


def test_update_nonexistent_category_for_item(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'name': 'modified_name',
        'category_id': 100
    }
    id = 7
    status_code = update_item(client, access_token, id, data)
    assert status_code == 404


def test_delete_non_existent_item(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = delete_item(client, access_token, 100)
    assert status_code == 404
