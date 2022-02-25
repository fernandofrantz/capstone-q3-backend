from flask import Blueprint
from app.controllers.orders_controller import create_orders

bp_orders = Blueprint('bp_orders', __name__, url_prefix='/api')

bp_orders.post('/orders')(create_orders)