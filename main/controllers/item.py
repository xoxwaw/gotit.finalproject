from flask import Blueprint, request, jsonify, abort

from main.auth import jwt_required
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.item import item_input_schema, item_output_schema, items_output_schema, item_pagination_schema

items = Blueprint('items', __name__)  # /items


@items.route('/', methods=['GET'])
def get_items():
    validate = item_pagination_schema.load(request.args)
    if len(validate.errors) > 0:
        abort(404, {'errors': validate.errors})
    query = ItemModel.query
    if validate.data.get('name') is not None:
        query = query.filter_by(name=validate.data.get('name'))
    if validate.data.get('category_id') is not None:
        query = query.filter_by(category_id=validate.data.get('category_id'))
    page = validate.data.get('page')
    per_page = validate.data.get('per_page')
    results = query.order_by(ItemModel.created_at.desc()) \
        .paginate(page, per_page, error_out=False)
    return jsonify({
        'items': items_output_schema.dump(results.items).data,
        'pages': results.pages,
        'total': results.total
    })


@items.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = ItemModel.query.get(item_id)
    if item is None:
        abort(404, {'message': 'item with id {} does not exist'.format(item_id)})
    return jsonify(item_output_schema.dump(item).data)


@items.route('/', methods=['POST'])
@jwt_required
def create_item(user_id):
    data = request.get_json()
    validate = item_input_schema.load(data)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors})
    user = UserModel.query.get(user_id)
    category_id = validate.data.get('category_id')
    category = None
    if category_id is not None:
        category = CategoryModel.query.get(category_id)
        if category and category.user_id != user_id:
            return abort(403, {'message': 'unauthorized to assign item to category with id {}'
                         .format(category_id)})
    item = ItemModel(user=user, category=category, **data)
    item.save_to_db()
    return jsonify({'message': 'item with name {} has been successfully created'.format(data.get('name'))})


@items.route('/<int:item_id>', methods=['PUT'])
@jwt_required
def update_item(user_id, item_id):
    data = request.get_json()
    validate = item_input_schema.load(data)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors})
    item = ItemModel.query.get(item_id)
    if item is None:
        abort(404, {'message': 'Cannot find item with id {}'.format(item_id)})
    if item.user_id != user_id:
        abort(403, {'message': 'Unauthorized to modify the content of this item'})
    category_id = validate.data.get('category_id')
    if category_id is not None:
        category = CategoryModel.query.get(category_id)
        if category is None:
            abort(404, {'message': 'category with id {} does not exist'.format(category_id)})
        if category.user_id != user_id:
            abort(403, {'message': 'Unauthorized to change to this category'})
    for key, val in validate.data.items():
        setattr(item, key, val)
    item.save_to_db()
    return '', 204


@items.route('/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_item(user_id, item_id):
    item = ItemModel.query.get(item_id)
    if item is None:
        abort(404, {'message': 'item with id {} does not exist'.format(item_id)})
    if item.user_id != user_id:
        abort(403, {'message': 'Forbidden'})
    item.delete_from_db()
    return '', 204
