from flask import jsonify, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import Forbidden

from app.configs.database import db
from app.models.purchases_model import PurchaseModel
from app.models.purchases_products_model import PurchaseProductModel
from app.services.customers_services import check_if_employee
from app.services.exceptions import (
    MissingPurchaseProductsListError as MissingList,
    InvalidPurchaseProductsListError as InvalidList,
    EmptyPurchaseProductListError as EmptyList,
    InvalidPurchaseProductFieldError as InvalidField,
    PurchaseProductNotFoundError as ProductNotFound,
    PurchaseNotFoundError as PurchaseNotFound
)

@jwt_required()
def create_purchase():
    try:
        check_if_employee(get_jwt_identity())
        data = request.get_json()
        session = db.session

        products_list = PurchaseModel.check_products_list(data['products'])
        purchase = PurchaseModel()

        for product in products_list:
            PurchaseModel.get_product(product.get('product_id'))
            product['purchase_id'] = purchase.id

            purchase_product = PurchaseProductModel(**product)
            purchase.products.append(purchase_product)

            inventory = PurchaseModel.get_inventory(purchase_product.product_id)
            inventory.quantity = inventory.quantity + purchase_product.quantity
            inventory.value = inventory.value + purchase_product.value

            session.add(inventory)

        session.add(purchase)
        session.commit()

        return jsonify(purchase), HTTPStatus.CREATED
    
    except Forbidden as e:
        return jsonify({"error": e.description}), e.code

    except KeyError:
        return jsonify(MissingList.response), MissingList.status_code

    except AttributeError:
        return jsonify(InvalidList.response), InvalidList.status_code

    except TypeError:
        return jsonify(InvalidField.response), InvalidField.status_code

    except InvalidField as e:
        return jsonify(e.response), e.status_code

    except ProductNotFound as e:
        return jsonify(e.response), e.status_code

    except EmptyList as e:
        return jsonify(e.response), e.status_code

@jwt_required()
def get_purchases():
    try:
        check_if_employee(get_jwt_identity())
        session = db.session
        base_query = session.query(PurchaseModel)

        purchases = base_query.all()

        return jsonify(purchases), 200

    except Forbidden as e:
        return jsonify({"error": e.description}), e.code

@jwt_required()
def get_purchase_by_id(purchase_id):
    try:
        check_if_employee(get_jwt_identity())
        session = db.session
        base_query = session.query(PurchaseModel)

        purchase = base_query.get(purchase_id)

        PurchaseModel.check_purchase(purchase)

        return jsonify(purchase), 200

    except Forbidden as e:
        return jsonify({"error": e.description}), e.code

    except PurchaseNotFound as e:
        return jsonify(e.response), e.status_code

@jwt_required()
def delete_purchase(purchase_id):
    try:
        check_if_employee(get_jwt_identity())
        session = db.session
        purchase_query = session.query(PurchaseModel)
        pur_prod_query = session.query(PurchaseProductModel)

        purchase = purchase_query.get(purchase_id)

        PurchaseModel.check_purchase(purchase)

        for purchase_product in purchase.products:
            inventory = PurchaseModel.get_inventory(purchase_product.product_id)
            inventory.quantity = inventory.quantity - purchase_product.quantity
            inventory.value = inventory.value - purchase_product.value

            session.add(inventory)

        pur_prods = pur_prod_query.filter_by(purchase_id=purchase_id).all()

        for pur_prod in pur_prods:
            session.delete(pur_prod)

        session.delete(purchase)
        session.commit()

        return '', 204

    except Forbidden as e:
        return jsonify({"error": e.description}), e.code
    
    except PurchaseNotFound as e:
        return jsonify(e.response), e.status_code