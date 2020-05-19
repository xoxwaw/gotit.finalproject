import pytest
import json

from main import create_app


def create_new_user():
    app = create_app()
    client = app.test_client()
    data = {
        "user": "test_user",
        "password": "test_password"
    }
    response = client.post('/register', data=json.dumps(data))
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert data['message'] == 'OK'


def test_auth_user():
    app = create_app()
    client = app.test_client()

    data = {
        "user": "test_user",
        "password": "test_password"
    }
    client.post('/register', data=json.dumps(data))
    response = client.post('/auth', data=json.dumps(data))
    data = json.loads(response.get_data(as_text=True))
    assert data['access_token'].count('.') == 2


