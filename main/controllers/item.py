from flask import Blueprint, request, jsonify

from main.schemas.item import item_input_schema, item_output_schema, items_output_schema
from main.schemas import query_validation_schema
from main.models.item import ItemModel
from main.models.user import UserModel
from main.models.category import CategoryModel
from main.auth import jwt_required

items = Blueprint('items', __name__, url_prefix='/items')


@items.route('/', methods=['GET'])
def get_items():
    validate = query_validation_schema.load(request.args)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
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
    validate = item_input_schema.load(data)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
    user = UserModel.query.get(user_id)
    category_id = data.get('category_id')
    category = None
    if category_id:
        category = CategoryModel.query.get(category_id)
        if category and category.creator_id != user_id:
            return jsonify({'message': 'unauthorized to assign item to category {}'
                           .format(category.name)}), 403
    item = ItemModel(user=user, category=category, **data)
    item.save_to_db()
    return jsonify({'message': 'item with name {} has been successfully created'.format(data.get('name'))}), 201


@items.route('/<id>', methods=['PUT'])
@jwt_required
def update_item(user_id, id):
    data = request.get_json()
    validate = item_input_schema.load(data)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
    item = ItemModel.query.get(id)
    if item:  # if item exists
        if item.creator_id != user_id:
            return jsonify({'message': 'Unauthorized to modify the content of this item'}), 403
        category_id = data.get('category_id')
        if category_id:
            category = CategoryModel.query.get(category_id)
            if category and category.creator_id != user_id:
                return jsonify({'message': 'Unauthorized to change the category of this item'}), 403
        for key in data:
            setattr(item, key, data[key])
    else:
        item = ItemModel(**data)
    item.save_to_db()
    return '', 204


@items.route('/<id>', methods=['DELETE'])
@jwt_required
def delete_item(user_id, id):
    item = ItemModel.query.get(id)
    if not item:
        return jsonify({'message': 'item with id {} does not exist'.format(id)}), 404
    if item.creator_id != user_id:
        return jsonify({'message': 'Unauthorized to modify the content of this item'}), 403
    item.delete_from_db()
    return '', 204
