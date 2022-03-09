from flask import Blueprint
from app.controllers.purchases_controller import create_purchase, delete_purchase, get_purchases, get_purchase_by_id

bp_purchase = Blueprint('bp_purchase', __name__, url_prefix='/purchases')

bp_purchase.post('')(create_purchase)
bp_purchase.get('')(get_purchases)
bp_purchase.get('<int:purchase_id>')(get_purchase_by_id)
bp_purchase.delete('<int:purchase_id>')(delete_purchase)