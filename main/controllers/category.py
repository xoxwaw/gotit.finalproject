from flask import Blueprint, request
from main.models.category import CategoryModel


categories = Blueprint('categories', __name__, url_prefix='/categories')


@categories.route('/', methods=['GET'], defaults={"page": 1})
@categories.route('/<int:page>')
def get_categories(page):
    name = request.args.get('name')
    query = CategoryModel.query
    per_page = 10
    if name:
        query = query.filter_by(name)
    query.paginate(page, per_page, error_out=False)
    


@categories.route('<int:id>', methods=['GET'])
def get_category_with_id(id):
    pass


@categories.route('/<int:id>', methods=['POST'])
def post_category():
    pass


@categories.route('/<id>', methods=['PUT'])
def update_category(id):
    pass


@categories.route('/<id>', methods=['DELETE'])
def delete_category(id):
    pass
