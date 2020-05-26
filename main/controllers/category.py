from flask import Blueprint, request, jsonify

from main.auth import jwt_required
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.category import category_input_schema, categories_output_schema, category_output_schema
from main.schemas import query_validation_schema

categories = Blueprint('categories', __name__, url_prefix='/categories')


@categories.route('/')
def get_categories():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    validate = query_validation_schema.load({
        'name': name,
        'page': page,
        'per_page': per_page
    })
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
    query = CategoryModel.query
    if name:
        query = query.filter_by(name=name)
    results = query.order_by(CategoryModel.created_at.desc()) \
        .paginate(page, per_page, error_out=False)
    return jsonify({
        'items': categories_output_schema.dump(results.items),
        'pages': results.pages,
        'total': results.total
    })


@categories.route('/<int:id>', methods=['GET'])
def get_category_with_id(id):
    category = CategoryModel.query.get(id)
    if not category:
        return {'message': 'category with id {} does not exist'.format(id)}, 404
    return jsonify(category_output_schema.dump(category))


@categories.route('/', methods=['POST'])
@jwt_required
def post_category(user_id):
    data = request.get_json()
    user = UserModel.query.get(user_id)
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
    category = CategoryModel(user=user, **data)
    category.save_to_db()
    return jsonify({'message': 'category with name {} has been successfully created'.format(data.get('name'))}), 201


@categories.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_category(user_id, id):
    data = request.get_json()
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        return jsonify(validate.errors), 400
    category = CategoryModel.query.get(id)
    if category:
        if category.creator_id != user_id:
            return jsonify({'message': 'Unauthorized to modify the content of this item'}), 403
        for key in data:
            setattr(category, key, data[key])
    else:
        category = CategoryModel(**data)
    category.save_to_db()
    return '', 204


@categories.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_category(user_id, id):
    category = CategoryModel.query.get(id)
    if not category:
        return jsonify({'message': 'Category with id {} does not exist'.format(id)}), 404
    if category.creator_id != user_id:
        return jsonify({'message': 'Unauthorized to modify this category'}), 403
    ItemModel.query.filter(ItemModel.category_id == category.id).delete()
    category.delete_from_db()
    return '', 204
