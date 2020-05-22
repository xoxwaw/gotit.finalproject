import pytest

from tests.helpers import (
    create_item,
    create_category,
    create_user
)


@pytest.fixture(scope="session", autouse=True)
def run_data(app):
    for i in range(3):
        user = {
            'username': 'user_test_{}'.format(i),
            'password': 'password'
        }
        create_user(user)
    for i in range(10):
        category = {
            'name': 'category_test_{}'.format(i),
            'creator_id': i % 3 + 1
        }
        create_category(category)
    for i in range(10):
        item = {
            'name': 'test_item_{}'.format(i),
            'creator_id': i % 3 + 1,
            'category_id': i % 10 + 1,
        }
        create_item(item)


