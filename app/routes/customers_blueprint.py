from flask import Blueprint
from app.controllers.customers_controller import create_customer

bp_customer = Blueprint('bp_customer', __name__, url_prefix='/api')

bp_customer.post('/customer')(create_customer)