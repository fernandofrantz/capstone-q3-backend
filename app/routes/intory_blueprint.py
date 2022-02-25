from flask import Blueprint
from app.controllers.intory_controller import create_inventory

bp_inventory = Blueprint('bp_inventory', __name__, url_prefix='/api')

bp_inventory.post('/inventory')(create_inventory)