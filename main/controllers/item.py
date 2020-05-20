from flask import Blueprint, request, jsonify

from main.schema.item import items_schema, item_schema
from main.models.item import ItemModel


items = Blueprint('items', __name__, url_prefix='/items')


@items.route('/', methods=['GET'])
def get_items():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = ItemModel.query
    if name:
        query = query.filter_by(name)
    results = query.order_by(ItemModel.created_at.desc()) \
        .paginate(page, per_page, error_out=False)
    return jsonify(items_schema.dump(results.items))


@items.route('<id>', methods=['GET'])
def get_item_with_id(id):
    result = ItemModel.get(ItemModel.id == id)
    if not result:
        return {'message': 'item with id {} does not exist'.format(id)}, 404
    return jsonify(item_schema.dump(result))


@items.route('/', methods=['POST'])
def post_item():
    pass


@items.route('/<id>', methods=['PUT'])
def update_item(id):
    pass


@items.route('/<id>', methods=['DELETE'])
def delete_item(id):
    pass
