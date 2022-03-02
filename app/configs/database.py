from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):

    db.init_app(app)

    app.db = db

    from app.models import CategoryModel
    from app.models import CustomerModel
    from app.models import InventoryModel
    from app.models import OrderModel
    from app.models import ProductModel
    from app.models import PurchaseModel

    from app.models.orders_products_model import orders_products
    from app.models.purchases_products_model import purchases_products