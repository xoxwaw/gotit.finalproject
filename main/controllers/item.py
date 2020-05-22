from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from main.schemas.item import item_input_schema, item_output_schema, items_output_schema
from main.schemas.validations.item import item_validation_schema
from main.models.item import ItemModel
from main.models.user import UserModel
from main.models.category import CategoryModel
from main.auth import jwt_required

items = Blueprint('items', __name__, url_prefix='/items')


@items.route('/', methods=['GET'])
def get_items():
    name = request.args.get('name')
    category_id = request.args.get('category_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        validation = item_validation_schema.load({
            'name': name,
            'category_id': category_id,
            'page': page,
            'per_page': per_page,
        })
    except ValidationError:
        return jsonify({'message': 'Wrong query format'}), 400
    query = ItemModel.query
    if name:
        query = query.filter_by(name)
    if category_id:
        query = query.filter_by(category_id)
    results = query.order_by(ItemModel.created_at.desc()) \
        .paginate(page, per_page, error_out=False)
    return jsonify({
        'items': items_output_schema.dump(results.items).data,
        'pages': results.pages,
        'total': results.total
    })


@items.route('/<id>', methods=['GET'])
def get_item_with_id(id):
    result = ItemModel.query.get(id)
    if not result:
        return {'message': 'item with id {} does not exist'.format(id)}, 404
    return jsonify(item_output_schema.dump(result).data)


@items.route('/', methods=['POST'])
@jwt_required
def post_item(user_id):
    data = request.get_json()
    try:
        item = item_input_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    user = UserModel.query.get(user_id)
    category_id = data.get('category_id')
    category = None
    if category_id:
        category = CategoryModel.query.get(category_id)
        if category and category.creator_id != user_id:
            return jsonify({'message': 'unauthorized to assign item to category {}'
                           .format(category.name)}), 403
    item = ItemModel(user=user, category=category, **data)
    ItemModel.save_to_db(item)
    return jsonify({'message': 'item with name {} has been successfully created'.format(data.get('name'))}), 201


@items.route('/<id>', methods=['PUT'])
@jwt_required
def update_item(user_id, id):
    data = request.get_json()
    try:
        item = item_input_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    item = ItemModel.query.get(id)
    if item:  # if item exists
        category_id = data.get('category_id')
        if category_id:
            category = CategoryModel.query.get(category_id)
            if category and category.creator_id != user_id:
                return jsonify({'message': 'Unauthorized to change the category of this item'}), 403
        if item.creator_id != user_id:
            return jsonify({'message': 'Unauthorized to modify the content of this item'}), 403
        for key in data:
            setattr(item, key, data[key])
    else:
        item = ItemModel(**data)
    item.save_to_db(item)
    return '', 204


@items.route('/<id>', methods=['DELETE'])
@jwt_required
def delete_item(user_id, id):
    item = ItemModel.query.get(id)
    if not item:
        return jsonify({'message': 'item with id {} does not exist'.format(id)}), 404
    if item.creator_id != user_id:
        return jsonify({'message': 'Unauthorized to modify the content of this item'}), 403
    ItemModel.delete_from_db(item)
    return '', 204
