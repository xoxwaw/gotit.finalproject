from main.libs.password import verify_password
from main.models.user import UserModel
from tests import TEST_PASSWORD, TEST_USERNAME
from tests.helpers import change_password, login

NEW_PASSWORD = 'new_password'


def test_change_password_successfully(access_token, client):
    data = {
        'old_password': TEST_PASSWORD,
        'new_password': NEW_PASSWORD
    }
    data, status_code = change_password(client, access_token, data)
    assert status_code == 204
    user = UserModel.query.filter_by(username=TEST_USERNAME).first()
    assert verify_password(NEW_PASSWORD, user.hashed_password, user.salt) is True


def test_wrong_old_password(client):
    access_token = login(client, TEST_USERNAME, NEW_PASSWORD)
    data = {
        'old_password': 'WRONG PASSWORD',
        'new_password': NEW_PASSWORD
    }
    data, status_code = change_password(client, access_token, data)
    assert status_code == 401
    assert data.get('message') == 'Wrong password'
    user = UserModel.query.filter_by(username=TEST_USERNAME).first()
    assert verify_password(NEW_PASSWORD, user.hashed_password, user.salt) is True


def test_invalid_new_password(client):
    access_token = login(client, TEST_USERNAME, NEW_PASSWORD)
    data = {
        'old_password': NEW_PASSWORD,
        'new_password': '222'
    }
    data, status_code = change_password(client, access_token, data)
    assert status_code == 400
