from flask import Blueprint
from app.controllers.products_controller import create_products, delete_products, get_products, get_products_by_id, patch_products

bp_products = Blueprint('bp_products', __name__, url_prefix='/products')

bp_products.post('')(create_products)
bp_products.get('')(get_products)
bp_products.get('<int:product_id>')(get_products_by_id)
bp_products.patch('<int:product_id>')(patch_products)
bp_products.delete('<int:product_id>')(delete_products)
