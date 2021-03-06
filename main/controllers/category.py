from flask import Blueprint, request, jsonify, abort

from main.auth import jwt_required
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.category import category_input_schema, categories_output_schema, category_output_schema
from main.schemas.pagination import pagination_schema

categories = Blueprint('categories', __name__)  # /categories


@categories.route('/')
def get_categories():
    validate = pagination_schema.load(request.args)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors})
    query = CategoryModel.query
    name = validate.data.get('name')
    page = validate.data.get('page')
    per_page = validate.data.get('per_page')
    if name:
        query = query.filter_by(name=name)
    results = query.order_by(CategoryModel.created_at.desc()) \
        .paginate(page, per_page, error_out=False)
    return jsonify({
        'items': categories_output_schema.dump(results.items),
        'pages': results.pages,
        'total': results.total
    })


@categories.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = CategoryModel.query.get(category_id)
    if not category:
        abort(404, {'message': 'category with id {} does not exist'.format(category_id)})
    return jsonify(category_output_schema.dump(category))


@categories.route('/', methods=['POST'])
@jwt_required
def create_category(user_id):
    data = request.get_json()
    user = UserModel.query.get(user_id)
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors})
    category = CategoryModel(user=user, **validate.data)
    category.save_to_db()
    return jsonify({
        'message': 'category with name {} has been successfully created'.format(validate.data.get('name'))})


@categories.route('/<int:category_id>', methods=['PUT'])
@jwt_required
def update_category(user_id, category_id):
    data = request.get_json()
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        abort(400, {'errors': validate.errors})
    category = CategoryModel.query.get(category_id)
    if category is None:
        abort(404, {'message': 'Cannot find category with id {}'.format(category_id)})
    if category.user_id != user_id:
        abort(403, {'message': 'Unauthorized to update this category'})
    for key, val in validate.data.items():
        setattr(category, key, val)
    category.save_to_db()
    return '', 204


@categories.route('/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(user_id, category_id):
    category = CategoryModel.query.get(category_id)
    if category is None:
        abort(404, {'message': 'Category with id {} does not exist'.format(category_id)})
    if category.user_id != user_id:
        abort(403, {'message': 'Unauthorized to modify this category'})
    ItemModel.query.filter(ItemModel.category_id == category.id).delete()
    category.delete_from_db()
    return '', 204
