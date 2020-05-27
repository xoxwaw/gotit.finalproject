import json

from main.libs.password import hash_password
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel

MIME_TYPE = 'application/json'
HEADERS = {
    'Content-Type': MIME_TYPE,
    'Accept': MIME_TYPE,
    'Authorization': 'JWT '
}


def login(client, username, password):
    response = client.post('/auth', data=json.dumps({
        'username': username, 'password': password
    }), headers=HEADERS)
    data = json.loads(response.get_data(as_text=True))
    return data.get('access_token')


def post_item(client, access_token, data):
    HEADERS['Authorization'] = 'JWT ' + access_token
    response = client.post('/items/', headers=HEADERS,
                           data=json.dumps(data))
    return response.status_code


def delete_item(client, access_token, id):
    HEADERS['Authorization'] = 'JWT ' + access_token
    response = client.delete('/items/{}'.format(id), headers=HEADERS)
    return response.status_code


def update_item(client, access_token, id, data):
    HEADERS['Authorization'] = 'JWT ' + access_token
    response = client.put('/items/{}'.format(id), headers=HEADERS, data=json.dumps(data))
    return response.status_code


def post_category(client, access_token, data):
    HEADERS['Authorization'] = 'JWT ' + access_token
    response = client.post('/categories/', headers=HEADERS,
                           data=json.dumps(data))
    return response.status_code


def delete_category(client, access_token, id):
    HEADERS['Authorization'] = 'JWT ' + access_token
    response = client.delete('/categories/{}'.format(id), headers=HEADERS)
    return response.status_code


def update_category(client, access_token, id, data):
    HEADERS['Authorization'] = 'JWT ' + access_token
    response = client.put('/categories/{}'.format(id), headers=HEADERS, data=json.dumps(data))
    return response.status_code


def create_category(data):
    category = CategoryModel(
        name=data['name'],
        description=data.get('description', None),
        creator_id=data['creator_id'],
    )
    CategoryModel.save_to_db(category)


def create_item(data):
    item = ItemModel(
        name=data['name'],
        description=data.get('description', ""),
        category_id=data.get('category_id'),
        creator_id=data['creator_id']
    )
    ItemModel.save_to_db(item)


def create_user(data):
    hashed_password, salt = hash_password(data['password'])
    user = UserModel(
        username=data['username'],
        hashed_password=hashed_password,
        salt=salt
    )
    UserModel.save_to_db(user)
