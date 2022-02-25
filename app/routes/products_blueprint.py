from flask import Blueprint
from app.controllers.products_controller import create_products

bp_products = Blueprint('bp_products', __name__, url_prefix='/api')

bp_products.post('/products')(create_products)