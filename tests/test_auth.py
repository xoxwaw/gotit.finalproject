import json

from tests import TEST_USERNAME, TEST_PASSWORD, TEST_UNAUTH_USER
from tests.helpers import login, post_category


MIME_TYPE = 'application/json'
HEADERS = {
    'Content-Type': MIME_TYPE,
    'Accept': MIME_TYPE
}


def test_register(client):
    response = client.post('/register', data=json.dumps({
        'username': TEST_UNAUTH_USER, 'password': TEST_PASSWORD
    }), headers=HEADERS)
    assert response.status_code == 204




def test_auth(client):
    token = login(client, TEST_USERNAME, TEST_PASSWORD)
    assert token.count('.') == 2


def test_empty_token(client):
    HEADERS['Authorization'] = ''
    data = {'name': 'test_item', 'description': 'a description'}
    response = client.post('/items/', headers=HEADERS,
                           data=json.dumps(data))
    assert response.status_code == 401


def test_wrong_token_format(client):
    data = {'name': 'phone book'}
    status_code = post_category(client, '', data)
    assert status_code == 401


def test_invalid_username(client):
    response = client.post('/auth', data=json.dumps({
        'username': 'wrong_username', 'password': TEST_PASSWORD
    }), headers=HEADERS)
    assert response.status_code == 401


def test_incorrect_access_token(client):
    data = {'name': 'phone book'}
    token = login(client, TEST_USERNAME, TEST_PASSWORD)
    status_code = post_category(client, token + 'a', data)
    assert status_code == 401


def test_bad_input_auth(client):
    data = {'username': 123, 'password': 'abc'}
    response = client.post('/auth', data=json.dumps(data))
    assert response.status_code == 400


def test_bad_input_register(client):
    data = {'username': 1223, 'password': 'aa'}
    response = client.post('/register', data=json.dumps(data))
    assert response.status_code == 400


def test_register_existing_user(client):
    data = {'username': TEST_USERNAME, 'password': 'a_valid_password'}
    response = client.post('/register', data=json.dumps(data))
    assert response.status_code == 400
