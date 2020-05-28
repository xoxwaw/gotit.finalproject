from tests.helpers import (
    post_item,
    delete_item,
    update_item,
)


def test_post_item_successfully(access_token, client):
    data = {'name': 'test_item'}
    data, status_code = post_item(client, access_token, data)
    assert status_code == 200


def test_update_item_successfully(access_token, client):
    data = {
        'name': 'modified_name'
    }
    item_id = 2
    data, status_code = update_item(client, access_token, item_id, data)
    assert status_code == 204


def test_delete_item_successfully(access_token, client):
    data, status_code = delete_item(client, access_token, 6)
    assert status_code == 204


def test_unauthorized_access_delete_item(unauth_token, client):
    data, status_code = delete_item(client, unauth_token, 3)
    assert status_code == 403
    assert data.get('message') == 'Forbidden'


def test_unauthorized_access_update_item(unauth_token, client):
    data = {
        'name': 'modified_name'
    }
    id = 8
    data, status_code = update_item(client, unauth_token, id, data)
    assert status_code == 403
    assert data.get('message') == 'Unauthorized to modify the content of this item'


def test_unauthorized_assign_category_of_item(unauth_token, client):
    data = {
        'name': 'invalid item',
        'category_id': 4
    }
    message, status_code = post_item(client, unauth_token, data)
    assert status_code == 403
    assert message == 'unauthorized to assign item to category with id {}'.format(4)


def test_post_invalid_format_category(access_token, client):
    data = {
        'name': 'new category',
        'category_id': 'hello'
    }
    data, status_code = post_item(client, access_token, data)
    assert status_code == 400


def test_get_items_successfully(client):
    response = client.get('/items/')
    assert response.status_code == 200


def test_get_nonexistent_item(client):
    response = client.get('/items/100')
    assert response.status_code == 404


def test_wrong_format_input_update_item(access_token, client):
    data = {
        'name': 0,
        'category_id': 2
    }
    data, status_code = update_item(client, access_token, 3, data)
    assert status_code == 400


def test_unauthorized_access_update_category_of_item(access_token, client):
    data = {
        'name': 'modified_name',
        'category_id': 11
    }
    item_id = 7
    data, status_code = update_item(client, access_token, item_id, data)
    assert status_code == 403
    assert data.get('message') == 'Unauthorized to change to this category'


def test_update_nonexistent_category_for_item(access_token, client):
    data = {
        'name': 'modified_name',
        'category_id': 100
    }
    item_id = 7
    data, status_code = update_item(client, access_token, item_id, data)
    assert status_code == 404
    assert data.get('message') == 'category with id {} does not exist'.format(100)


def test_delete_non_existent_item(access_token, client):
    data, status_code = delete_item(client, access_token, 100)
    assert status_code == 404
    assert data.get('message') == 'item with id {} does not exist'.format(100)
