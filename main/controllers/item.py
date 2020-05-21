import datetime as dt
import sys

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from main.schema.item import item_input_schema, item_output_schema, items_output_schema
from main.models.item import ItemModel
from main.auth import jwt_required


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
    return jsonify(items_output_schema.dump(results.items).data)


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
    data['creator_id']=user_id
    data['created_at']=dt.datetime.utcnow()
    data['updated_at']=dt.datetime.utcnow()
    try:
        item = item_input_schema.load(data)
        print(item, file=sys.stderr)
    except ValidationError as err:
        return jsonify(err.messages), 422
    item = ItemModel(**data)
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
    data['updated_at'] = dt.datetime.utcnow()
    if item:
        if item.creator_id == user_id:
            for key in data:
                setattr(item, key, data[key])
        else:
            return jsonify({'Unauthorized to modify the content of this item'}), 403
    else:
        data['created_at'] = dt.datetime.utcnow()
        item = ItemModel(**data)
    item.save_to_db(item)
    return '', 204


@items.route('/<id>', methods=['DELETE'])
@jwt_required
def delete_item(user_id, id):
    item = ItemModel.query.get(id)
    if not item:
        return jsonify({'message': 'item with id {} does not exist'.format(id)}), 404
    if item.id != user_id:
        return jsonify({'Unauthorized to modify the content of this item'}), 403
    ItemModel.delete_from_db(item)
    return '', 204
