from flask import jsonify, request, current_app

from app.configs.database import db
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
        return jsonify(new_product), 201
    except:
        return jsonify(), 404


def get_products():
    session = db.session
    base_query = session.query(ProductModel)

    products = base_query.all()

    return jsonify(products), 200

def get_product_by_id(product_id):
    session = db.session
    base_query = session.query(ProductModel)

    products = base_query.get_or_404(products_id)

    return jsonify(products), 200

def patch_product(product_id):
    return f'funciona, id {product_id}', 200