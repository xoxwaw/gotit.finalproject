from flask import Blueprint, request, jsonify, abort

from main.auth import jwt_required
from main.constants import (BAD_REQUEST, UNAUTHORIZED, NOT_FOUND, NO_CONTENT)
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.schemas.category import category_input_schema, categories_output_schema, category_output_schema
from main.schemas.query import query_validation_schema

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
        abort(BAD_REQUEST, validate.errors)
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


@categories.route('/<int:category_id>', methods=['GET'])
def get_category_with_id(category_id):
    category = CategoryModel.query.get(category_id)
    if not category:
        abort(404, 'category with id {} does not exist'.format(category_id))
    return jsonify(category_output_schema.dump(category))


@categories.route('/', methods=['POST'])
@jwt_required
def post_category(user_id):
    data = request.get_json()
    user = UserModel.query.get(user_id)
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        return abort(BAD_REQUEST, validate.errors)
    category = CategoryModel(creator=user, **data)
    category.save_to_db()
    return jsonify({
        'message': 'category with name {} has been successfully created'.format(data.get('name'))})


@categories.route('/<int:category_id>', methods=['PUT'])
@jwt_required
def update_category(user_id, category_id):
    data = request.get_json()
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        abort(BAD_REQUEST, validate.errors)
    category = CategoryModel.query.get(category_id)
    if category:
        if category.creator_id != user_id:
            abort(UNAUTHORIZED, 'Unauthorized to modify the content of this item')
        for key, val in data.items():
            setattr(category, key, val)
    else:
        category = CategoryModel(**data)
    category.save_to_db()
    return '', 204


@categories.route('/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(user_id, category_id):
    category = CategoryModel.query.get(category_id)
    if not category:
        abort(NOT_FOUND, 'Category with id {} does not exist'.format(category_id))
    if category.creator_id != user_id:
        abort(UNAUTHORIZED, 'Unauthorized to modify this category')
    ItemModel.query.filter(ItemModel.category_id == category.id).delete()
    category.delete_from_db()
    return '', NO_CONTENT
