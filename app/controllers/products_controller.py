from flask import jsonify, request, current_app
from http import HTTPStatus
from app.configs.database import db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.services.validations import check_valid_patch
from app.models.products_model import ProductModel
from app.models.inventory_model import InventoryModel
from app.models.categories_model import CategoryModel


def create_product():
    try:
        data = request.get_json()

        valid_keys = ["name", "category", "description", "price"]
        check_valid_patch(data, valid_keys)

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
        
    except KeyError:
        data = request.get_json()
        for key in data.keys():
            if key != 'name' and key != 'price' and key != 'description' and key != 'category':
                wrong_key = key
        return {"available_keys": ["name", "price", "description", "category"], "wrong_keys_sended":[wrong_key]}, HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST

    except TypeError as err:
        return jsonify(err.args[0]), 400

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

        valid_keys = ["name", "category", "description", "price"]
        check_valid_patch(data, valid_keys)

        category = CategoryModel.query.filter_by(name=data["category"]).first()
        if category == None:
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
        return {"msg": "product not found!"}, HTTPStatus.NOT_FOUND
    except KeyError:
        valid_keys = {"name": str, "price": float, "description": str, "category_id": str}
        return {"invalid_keys": [
            {"sent_keys": 
                list(data.keys())
            }, 
            {"valid_keys": 
                list(valid_keys.keys())
            }
        ]}, HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST

    except TypeError as err:
        return jsonify(err.args[0]), 400