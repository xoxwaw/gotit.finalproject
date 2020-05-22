import pytest

from tests.helpers import (
    create_item,
    create_category,
    create_user
)


def populate_data():
    user = {
        'username': 'user_test',
        'password': 'password'
    }
    create_user(user)
    for i in range(10):
        category = {
            'name': 'category_test_{}'.format(i),
            'creator_id': 1
        }
        create_category(category)
    for i in range(10):
        item = {
            'name': 'test_item_{}'.format(i),
            'creator_id': 1,
            'category_id': i % 10 + 1,
        }
        create_item(item)
