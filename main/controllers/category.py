import datetime as dt
import sys

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from main.schema.category import category_input_schema, categories_output_schema, category_output_schema
from main.models.category import CategoryModel
from main.models.item import ItemModel
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
    return jsonify(categories_output_schema.dump(results.items))
    


@categories.route('<int:id>', methods=['GET'])
def get_category_with_id(id):
    result = CategoryModel.get(CategoryModel.id == id)
    if not result:
        return {'message': 'category with id {} does not exist'.format(id)}, 404
    return jsonify(category_output_schema.dump(result))



@categories.route('/', methods=['POST'])
@jwt_required
def post_category(user_id):
    data = request.get_json()
    data['creator_id'] = user_id
    try:
        category = category_input_schema.load(data)
        print(category, file=sys.stderr)
    except ValidationError as err:
        return jsonify(err.messages), 422

    category = CategoryModel(**data)
    category.save_to_db(category)
    return jsonify({'message': 'category with name {} has been successfully created'.format(data.get('name'))}), 201


@categories.route('/<id>', methods=['PUT'])
@jwt_required
def update_category(user_id, id):
    data = request.get_json()
    try:
        category = category_input_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    category = CategoryModel.query.get(id)
    if category:
        if category.creator_id == user_id:
            for key in data:
                setattr(category, key, data[key])
        else:
            return jsonify({'Unauthorized to modify the content of this item'}), 403
    else:
        category = CategoryModel(**data)
    CategoryModel.save_to_db(category)
    return '', 204


@categories.route('/<id>', methods=['DELETE'])
@jwt_required
def delete_category(user_id, id):
    category = CategoryModel.query.get(id)
    if not category:
        return jsonify({'Category with id {} does not exist'.format(id)}), 404
    if category.creator_id != user_id:
        return jsonify({'Unauthorized to modify this category'}), 403
    ItemModel.query.filter(ItemModel.category_id == category.id).delete()
    CategoryModel.delete_from_db(category)
    return '', 204
