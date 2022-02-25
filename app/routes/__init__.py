from flask import Flask
from app.routes.categories_blueprint import bp_category
from app.routes.customers_blueprint import bp_customer
from app.routes.intory_blueprint import bp_inventory
from app.routes.orders_blueprint import bp_orders
from app.routes.products_blueprint import bp_products
from app.routes.order_product_blueprint import bp_create_order
from app.routes.purchase_products_blueprint import bp_purchase_products

def init_app(app: Flask):
    app.register_blueprint(bp_category)
    app.register_blueprint(bp_customer)
    app.register_blueprint(bp_create_order)
    app.register_blueprint(bp_inventory)
    app.register_blueprint(bp_orders)
    app.register_blueprint(bp_products)
    app.register_blueprint(bp_purchase_products)
