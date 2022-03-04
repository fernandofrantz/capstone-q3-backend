from flask import jsonify, request

from app.configs.database import db
from app.models.purchases_model import ProductsModel

def create_product():
    data = request.get_json()
    session = db.session

    products = ProductsModel

    return jsonify(user), 201

def get_products():
    session = db.session
    base_query = session.query(ProductsModel)

    purchases = base_query.all()

    return jsonify(products), 200

def get_product_by_id(product_id):
    session = db.session
    base_query = session.query(ProductsModel)

    purchase = base_query.get_or_404(products_id)

    return jsonify(products), 200

def patch_product(product_id):
    return f'funciona, id {product_id}', 200