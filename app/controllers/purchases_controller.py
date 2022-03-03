from flask import jsonify, request
from werkzeug.exceptions import NotFound

from app.configs.database import db
from app.models.purchases_model import PurchaseModel
from app.models.purchases_products_model import PurchaseProductModel

def create_purchase():
    data = request.get_json()
    session = db.session

    purchase = PurchaseModel()

    for product in data['products']:
        PurchaseModel.get_product(product["product_id"])
        product['purchase_id'] = purchase.id

        purchase_product = PurchaseProductModel(**product)
        purchase.products.append(purchase_product)

        inventory = PurchaseModel.get_inventory(purchase_product.product_id)
        inventory.quantity = inventory.quantity + purchase_product.quantity
        inventory.value = inventory.value + purchase_product.value

        session.add(inventory)

    session.add(purchase)
    session.commit()

    return jsonify(purchase), 201

def get_purchases():
    session = db.session
    base_query = session.query(PurchaseModel)

    purchases = base_query.all()

    return jsonify(purchases), 200

def get_purchase_by_id(purchase_id):
    session = db.session
    base_query = session.query(PurchaseModel)

    purchase = base_query.get_or_404(purchase_id)

    return jsonify(purchase), 200

def delete_purchase(purchase_id):
    session = db.session
    base_query = session.query(PurchaseModel)

    purchase = base_query.get_or_404(purchase_id)

    for purchase_product in purchase.products:
        inventory = PurchaseModel.get_inventory(purchase_product.product_id)
        inventory.quantity = inventory.quantity - purchase_product.quantity
        inventory.value = inventory.value - purchase_product.value

        session.add(inventory)

    session.delete(purchase)
    session.commit()

    return '', 204