import logging
import sys

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from main.schema.category import category_schema, categories_schema
from main.models.category import CategoryModel
from main.auth import jwt_required


categories = Blueprint('categories', __name__, url_prefix='/categories')


@categories.route('/')
def get_categories():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = CategoryModel.query
    if name:
        query = query.filter_by(name)
    results = query.order_by(CategoryModel.created_at.desc())\
        .paginate(page, per_page, error_out=False)
    return jsonify(categories_schema.dump(results.items))
    


@categories.route('<int:id>', methods=['GET'])
def get_category_with_id(id):
    result = CategoryModel.get(CategoryModel.id == id)
    if not result:
        return {'message': 'category with id {} does not exist'.format(id)}, 404
    return jsonify(category_schema.dump(result))



@categories.route('/', methods=['POST'])
@jwt_required
def post_category(user_id):
    data = request.get_json()
    data['creator_id'] = user_id
    try:
        category = category_schema.load(data)
        print(category, file=sys.stderr)
    except ValidationError as err:
        return jsonify(err.messages), 422

    category = CategoryModel(**data)
    category.save_to_db(category)
    return jsonify({'message': 'category with name {} has been successfully created'.format(data.get('name'))}), 201


@categories.route('/<id>', methods=['PUT'])
@jwt_required
def update_category(id):
    pass


@categories.route('/<id>', methods=['DELETE'])
@jwt_required
def delete_category(id):
    pass
