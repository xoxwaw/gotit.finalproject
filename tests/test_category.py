from main.models.category import CategoryModel
from tests.helpers import (
    post_category,
    delete_category,
    update_category,
)


def test_create_category_successfully(unauth_token, client):
    data = {'name': 'test_category', 'description': 'This is a very nice category.'}
    data, status_code = post_category(client, unauth_token, data)
    assert status_code == 200
    assert CategoryModel.query.filter_by(name='test_category').first() is not None


def test_update_category_successfully(access_token, client):
    data = {
        'name': 'modified_name'
    }
    category_id = 1
    data, status_code = update_category(client, access_token, category_id, data)
    assert status_code == 204
    category = CategoryModel.query.get(category_id)
    assert category.name == 'modified_name'


def test_delete_category_successfully(access_token, client):
    category_id = 1
    data, status_code = delete_category(client, access_token, category_id)
    assert status_code == 204
    assert CategoryModel.query.get(category_id) is None


def test_unauthorized_access_delete_category(unauth_token, client):
    category_id = 3
    data, status_code = delete_category(client, unauth_token, category_id)
    assert status_code == 403
    assert data.get('message') == 'Unauthorized to modify this category'
    assert CategoryModel.query.get(category_id) is not None


def test_unauthorized_access_update_category(unauth_token, client):
    data = {
        'name': 'modified_name',
    }
    category_id = 8
    data, status_code = update_category(client, unauth_token, category_id, data)
    assert status_code == 403
    assert data.get('message') == 'Unauthorized to update this category'
    category = CategoryModel.query.get(category_id)
    assert category.name != 'modified_name'


def test_invalid_format_post_category(unauth_token, client):
    data = {
        'name': 0
    }
    data, status_code = post_category(client, unauth_token, data)
    assert status_code == 400


def test_get_categories(client):
    response = client.get('/categories/')
    assert response.status_code == 200


def test_blank_name_categories(unauth_token, client):
    data = {
        'name': '         ',
        'description': 'filled with spaces'
    }
    data, status_code = post_category(client, unauth_token, data)
    assert status_code == 400
