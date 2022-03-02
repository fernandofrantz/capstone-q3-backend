from flask import Blueprint
from app.controllers.categories_controller import create_category, get_category, patch_category

bp_category = Blueprint('bp_category', __name__, url_prefix='/category')

bp_category.get('')(create_category)
bp_category.get('<int:category_id>')(get_category)
bp_category.patch('<int:category_id>')(patch_category)
