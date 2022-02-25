from flask import Blueprint
from app.controllers.order_product_controller import create_order_product

bp_create_order = Blueprint('bp_create_order', __name__, url_prefix='/api')

bp_create_order.post('/create_order')(create_order_product)