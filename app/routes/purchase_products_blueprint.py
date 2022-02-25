from flask import Blueprint
from app.controllers.purchase_products_controller import create_purchase_products

bp_purchase_products = Blueprint('bp_purchase_products', __name__, url_prefix='/api')

bp_purchase_products.post('/purchase_products')(create_purchase_products)