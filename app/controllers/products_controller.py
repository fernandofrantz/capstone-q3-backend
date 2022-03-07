from flask import jsonify, request, current_app
from http import HTTPStatus
from app.configs.database import db

from werkzeug.exceptions import NotFound
from app.services.validations import check_valid_patch
from app.models.products_model import ProductModel
from app.models.inventory_model import InventoryModel
from app.models.categories_model import CategoryModel


def create_product():
    try:
        data = request.get_json()
        category = CategoryModel.query.filter_by(name=data["category"]).first()
        if category == None:
            category = CategoryModel(**{"name":data["category"]})
            current_app.db.session.add(category)
            current_app.db.session.commit()
        data["category_id"] = category.id
        del data["category"]
        new_product = ProductModel(**data)
        current_app.db.session.add(new_product)
        current_app.db.session.commit()
        new_inventory = InventoryModel(**{"product_id": new_product.id, "quantity": 0, "value": 0})
        current_app.db.session.add(new_inventory)    

        current_app.db.session.commit()
        return jsonify(new_product), HTTPStatus.OK
    except ValueError:
        return {'error':'the type name is not a string'}, HTTPStatus.BAD_REQUEST

def get_products():
    session = db.session
    base_query = session.query(ProductModel)

    products = base_query.all()

    return jsonify(products), HTTPStatus.OK

def get_product_by_id(product_id):
    try:
        product = ProductModel.query.get_or_404(product_id)
        return jsonify(product), HTTPStatus.OK
    except NotFound:
        return {"msg": "product not found!"}, HTTPStatus.NOT_FOUND

def patch_product(product_id):
    try:
        data = request.get_json()
        product = ProductModel.query.get_or_404(product_id)

        valid_keys = ["name", "category_id", "description", "price"]
        check_valid_patch(data, valid_keys)

        for key, name in data.items():
            setattr(product, key, name)
        for key, category_id in data.items():
            setattr(product, key, category_id)
        for key, price in data.items():
            setattr(product, key, price)
        for key, description in data.items():
            setattr(product, key, description)

        current_app.db.session.add(product)
        current_app.db.session.commit()

        return jsonify(product), HTTPStatus.OK

    except NotFound:
        return {"msg": "product not found!"}, HTTPStatus.NOT_FOUND
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST
    except TypeError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST
