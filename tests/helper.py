import json
from datetime import datetime as dt

from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


TEST_USERNAME = 'user_test'
TEST_PASSWORD = 'password'


def login(client, username, password):
    response = client.post('/auth', data={
        'username': username, 'password': password
    })
    data = json.loads(response.get_data(as_text=True))
    return data


def post_item(client, access_token, data):
    response = client.post('/items', headers={'Authorization': access_token},
                data=data)
    return response.status_code


def post_category(client, access_token, data):
    response = client.post('/categories', headers={'Authorization': access_token},
                           data=data)
    return response.status_code


def create_category(data):
    category = CategoryModel(
        name=data['name'],
        description=data.get('description', None),
        creator_id=data['creator_id'],
        created_at=dt.utcnow(),
        updated_at=dt.utcnow()
    )
    CategoryModel.save_to_db(category)


def create_item(data):
    item = ItemModel(
            name=data['name'],
            description=data.get('description', ""),
            category_id=data.get('category_id', None),
            creator_id=data['creator_id'],
            created_at=dt.utcnow(),
            updated_at=dt.utcnow()
        )
    ItemModel.save_to_db(item)


def create_user(data):
    user = UserModel(
        username=data['username'],
        hashed_password=data['hashed_password'],
        salt=data['salt'],
        created_at=dt.utcnow(),
        updated_at=dt.utcnow()
    )
    UserModel.save_to_db(user)