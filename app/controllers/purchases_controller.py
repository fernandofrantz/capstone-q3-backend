from flask import jsonify, request

from app.configs.database import db
from app.models.purchases_model import PurchaseModel
from app.models.purchases_products_model import PurchaseProductModel

def create_purchase():
    data = request.get_json()
    session = db.session

    purchase = PurchaseModel()

    for product in data['products']:
        PurchaseModel.get_product(product)
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
    return 'funciona', 200

def get_purchase_by_id(purchase_id):
    return f'funciona, id: {purchase_id}', 200

def patch_purchase(purchase_id):
    return f'funciona, id: {purchase_id}', 200

def delete_purchase(purchase_id):
    return f'funciona, id: {purchase_id}', 200