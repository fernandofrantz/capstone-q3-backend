from flask import Flask, Blueprint
from app.routes.purchase_products_blueprint import bp_purchase_products
from app.routes.categories_blueprint import bp_category
from app.routes.customers_blueprint import bp_customer
from app.routes.products_blueprint import bp_products
from app.routes.intory_blueprint import bp_inventory
from app.routes.orders_blueprint import bp_orders

bp_api = Blueprint("api", __name__, url_prefix="/")

def init_app(app: Flask):
    bp_api.register_blueprint(bp_purchase_products)
    bp_api.register_blueprint(bp_inventory)
    bp_api.register_blueprint(bp_products)
    bp_api.register_blueprint(bp_category)
    bp_api.register_blueprint(bp_customer)
    bp_api.register_blueprint(bp_orders)

    app.register_blueprint(bp_api)