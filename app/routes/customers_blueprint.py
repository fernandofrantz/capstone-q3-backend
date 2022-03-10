from app.controllers.customers_controller import sign_in, sign_up, patch_user
from flask import Blueprint

bp_customer = Blueprint('bp_customer', __name__, url_prefix='/user')

bp_customer.post('/signin')(sign_in)
bp_customer.post('/signup')(sign_up)
bp_customer.patch('')(patch_user)