from flask import request, current_app, jsonify
from app.models import InventoryModel
from werkzeug.exceptions import NotFound


def get_inventory():
    inventory = InventoryModel.query.all()
    return jsonify(inventory), 200

def get_inventory_by_id(inventory_id):
    try:
        inventory_item = InventoryModel.query.get_or_404(inventory_id)
        return jsonify(inventory_item), 200
    except NotFound:
        return {"msg": "product not found!"}, 404

def patch_inventory(inventory_id):
    try:
        data = request.get_json()
        inventory_item = InventoryModel.query.get_or_404(inventory_id)

        for key, value in data.items():
            setattr(inventory_item, key, value)

        current_app.db.session.add(inventory_item)
        current_app.db.session.commit()


        return jsonify(inventory_item), 200

    except NotFound:
        return {"msg": "product not found!"}, 404

def delete_inventory(inventory_id):
    try:
        inventory_item = InventoryModel.query.get_or_404(inventory_id)
        setattr(inventory_item, "value", 0)
        setattr(inventory_item, "quantity", 0)
        current_app.db.session.add(inventory_item)
        current_app.db.session.commit()
        
        return jsonify(inventory_item), 200

    except NotFound:
        return {"msg": "product not found!"}, 404

