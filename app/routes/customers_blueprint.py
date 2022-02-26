from flask import Blueprint
from app.controllers.customers_controller import sign_in, sign_up

bp_customer = Blueprint('bp_customer', __name__, url_prefix='/api')

bp_customer.post('/signup')(sign_up)
bp_customer.post('/signin')(sign_in)