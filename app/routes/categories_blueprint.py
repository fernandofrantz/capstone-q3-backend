from flask import Blueprint
from app.controllers.categories_controller import get_categories, get_category_by_id, patch_category

bp_categories = Blueprint('bp_categories', __name__, url_prefix='/categories')

bp_categories.get('')(get_categories)
bp_categories.get('<int:category_id>')(get_category_by_id)
bp_categories.patch('<int:category_id>')(patch_category)
