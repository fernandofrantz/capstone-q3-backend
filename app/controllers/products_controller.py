from flask import jsonify, request, current_app
from http import HTTPStatus
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.services.validations import check_valid_patch
from app.models.products_model import ProductModel
from app.models.inventory_model import InventoryModel
from app.models.categories_model import CategoryModel
from app.models.customers_model import CustomerModel
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def create_product():
    user_identity = get_jwt_identity()
    if not CustomerModel.query.get(user_identity.get('id')).employee:
        return {"msg": "unauthorized"}, 401
    try:
        data = request.get_json()

        valid_keys = ["name", "category", "description", "price"]
        check_valid_patch(data, valid_keys)

        category = CategoryModel.query.filter_by(name=data["category"].lower()).first()
        if category == None:
            category = CategoryModel(**{"name":data["category"].lower()})
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
        
    except KeyError:
        return {"required_keys": ["name", "price", "description", "category"], "recieved_keys": list(data.keys())}, HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST

    except TypeError as err:
        return jsonify(err.args[0]), 400

def get_products():
    session = db.session
    base_query = session.query(ProductModel)

    products = base_query.all()

    return jsonify({"products": products}), HTTPStatus.OK

def get_product_by_id(product_id):
    try:
        product = ProductModel.query.get_or_404(product_id)
        return jsonify(product), HTTPStatus.OK
    except NotFound:
        return {"msg": f"product id {product_id} not found"}, HTTPStatus.NOT_FOUND

@jwt_required()
def patch_product(product_id):
    user_identity = get_jwt_identity()
    if not CustomerModel.query.get(user_identity.get('id')).employee:
        return {"msg": "unauthorized"}, 401
    try:
        data = request.get_json()
        product = ProductModel.query.get_or_404(product_id)

        valid_keys = ["name", "category", "description", "price"]
        check_valid_patch(data, valid_keys)

        category = CategoryModel.query.filter_by(name=data.get("category", "").lower()).first()

        if category is not None:
            data["category_id"] = category.id
            del data["category"]

        if category == None and data.get("category"):
            category = CategoryModel(**{"name":data["category"]})
            current_app.db.session.add(category)
            current_app.db.session.commit()
            data["category_id"] = category.id
            del data["category"]

        for key, name in data.items():
            setattr(product, key, name)

        current_app.db.session.add(product)
        current_app.db.session.commit()

        return jsonify(product), HTTPStatus.OK

    except NotFound:
        return {"error": f"product id {product_id} not found"}, HTTPStatus.NOT_FOUND
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST

    except TypeError as err:
        return jsonify({"error": err.args[0]}), 400