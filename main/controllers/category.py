from flask import Blueprint, request, jsonify

from main.auth import jwt_required
from main.constants import NO_CONTENT
from main.controllers.errors import (BadRequest, Forbidden, NotFound)
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
        return BadRequest(message=validate.errors).to_json()
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
        return NotFound(message='category with id {} does not exist'.format(category_id)).to_json()
    return jsonify(category_output_schema.dump(category))


@categories.route('/', methods=['POST'])
@jwt_required
def post_category(user_id):
    data = request.get_json()
    user = UserModel.query.get(user_id)
    validate = category_input_schema.load(data)
    if len(validate.errors) > 0:
        return BadRequest(message=validate.errors).to_json()
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
        return BadRequest(message=validate.errors).to_json()
    category = CategoryModel.query.get(category_id)
    if category:
        if category.creator_id != user_id:
            return Forbidden(message='Unauthorized to modify the content of this item').to_json()
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
        return NotFound(message='Category with id {} does not exist'.format(category_id)).to_json()
    if category.creator_id != user_id:
        return Forbidden(message='Unauthorized to modify this category').to_json()
    ItemModel.query.filter(ItemModel.category_id == category.id).delete()
    category.delete_from_db()
    return '', NO_CONTENT
