from flask import Blueprint, request

from main.models.item import ItemModel, item_schema, items_schema


items = Blueprint('items', __name__, url_prefix='/items')


@items.route('/', methods=['GET'])
def get_items():

    pass


@items.route('<id>', methods=['GET'])
def get_item_with_id(id):
    pass


@items.route('/', methods=['POST'])
def post_item():
    pass


@items.route('/<id>', methods=['PUT'])
def update_item(id):
    pass


@items.route('/<id>', methods=['DELETE'])
def delete_item(id):
    pass
