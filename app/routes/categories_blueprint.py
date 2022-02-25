from flask import Blueprint
from app.controllers.categories_controller import create_category

bp_category = Blueprint('bp_category', __name__, url_prefix='/api')

bp_category.post('/category')(create_category)