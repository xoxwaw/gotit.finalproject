from tests import TEST_PASSWORD, TEST_USERNAME
from tests.helpers import change_password, login

NEW_PASSWORD = 'new_password'


def test_change_password(client):
    access_token = login(client, TEST_USERNAME, TEST_PASSWORD)
    data = {
        'old_password': TEST_PASSWORD,
        'new_password': NEW_PASSWORD
    }
    status_code = change_password(client, access_token, data)
    assert status_code == 204


def test_wrong_old_password(client):
    access_token = login(client, TEST_USERNAME, NEW_PASSWORD)
    data = {
        'old_password': 'WRONG PASSWORD',
        'new_password': NEW_PASSWORD
    }
    status_code = change_password(client, access_token, data)
    assert status_code == 401


def test_invalid_new_password(client):
    access_token = login(client, TEST_USERNAME, NEW_PASSWORD)
    data = {
        'old_password': NEW_PASSWORD,
        'new_password': '222'
    }
    status_code = change_password(client, access_token, data)
    assert status_code == 400
