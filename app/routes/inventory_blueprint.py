from flask import Blueprint
from app.controllers.inventory_controller import delete_inventory, get_inventory, get_inventory_by_id, patch_inventory

bp_inventory = Blueprint('bp_inventory', __name__, url_prefix='/inventory')

bp_inventory.get('')(get_inventory)
bp_inventory.get('<int:inventory_id>')(get_inventory_by_id)
bp_inventory.patch('<int:inventory_id>')(patch_inventory)
bp_inventory.delete('<int:inventory_id>')(delete_inventory)
