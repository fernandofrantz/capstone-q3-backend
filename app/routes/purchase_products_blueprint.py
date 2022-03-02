from flask import Blueprint
from app.controllers.purchase_products_controller import create_purchase, delete_purchase, get_purchase, get_purchase_by_id, patch_purchase

bp_purchase_products = Blueprint('bp_purchase_products', __name__, url_prefix='/purchase')

bp_purchase_products.post('')(create_purchase)
bp_purchase_products.get('')(get_purchase)
bp_purchase_products.get('<int:purchase_id>')(get_purchase_by_id)
bp_purchase_products.patch('<int:purchase_id>')(patch_purchase)
bp_purchase_products.delete('<int:purchase_id>')(delete_purchase)