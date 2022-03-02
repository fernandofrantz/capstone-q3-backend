from flask import Blueprint
from app.controllers.orders_controller import create_order, delete_product, get_order, get_order_by_id, patch_product

bp_orders = Blueprint('bp_orders', __name__, url_prefix='/orders')

bp_orders.post('')(create_order)
bp_orders.get('')(get_order)
bp_orders.get('<int:order_id>')(get_order_by_id)
bp_orders.patch('<int:order_id>')(patch_product)
bp_orders.delete('<int:order_id>')(delete_product)