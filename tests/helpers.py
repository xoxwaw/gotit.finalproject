import json

from main.libs.password import encoder
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype,
    'Authorization': 'JWT '
}


def login(client, username, password):
    response = client.post('/auth', data=json.dumps({
        'username': username, 'password': password
    }), headers=headers)
    data = json.loads(response.get_data(as_text=True))
    return data.get('access_token')


def post_item(client, access_token, data):
    headers['Authorization'] = 'JWT ' + access_token
    response = client.post('/items/', headers=headers,
                           data=json.dumps(data))
    return response.status_code


def delete_item(client, access_token, id):
    headers['Authorization'] = 'JWT ' + access_token
    response = client.delete('/items/{}'.format(id), headers=headers)
    return response.status_code


def update_item(client, access_token, id, data):
    headers['Authorization'] = 'JWT ' + access_token
    response = client.put('/items/{}'.format(id), headers=headers, data=json.dumps(data))
    return response.status_code


def post_category(client, access_token, data):
    headers['Authorization'] = 'JWT ' + access_token
    response = client.post('/categories/', headers=headers,
                           data=json.dumps(data))
    return response.status_code


def delete_category(client, access_token, id):
    headers['Authorization'] = 'JWT ' + access_token
    response = client.delete('/categories/{}'.format(id), headers=headers)
    return response.status_code


def update_category(client, access_token, id, data):
    headers['Authorization'] = 'JWT ' + access_token
    response = client.put('/categories/{}'.format(id), headers=headers, data=json.dumps(data))
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
    hashed_password, salt = encoder(data['password'])
    user = UserModel(
        username=data['username'],
        hashed_password=hashed_password,
        salt=salt
    )
    UserModel.save_to_db(user)
