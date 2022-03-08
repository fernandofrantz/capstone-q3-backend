from flask import request, current_app, jsonify
from app.models import InventoryModel
from werkzeug.exceptions import NotFound
from app.services.validations import check_valid_patch


def get_inventory():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 15))
    start = (page - 1) * per_page if page > 0 else 0
    end = per_page + start
    inventory = InventoryModel.query.all()[start:end]
    return jsonify({"page": page, "per_page": per_page, "data": inventory}), 200

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

        valid_keys = ["value", "quantity"]
        check_valid_patch(data, valid_keys)

        for key, value in data.items():
            setattr(inventory_item, key, value)

        current_app.db.session.add(inventory_item)
        current_app.db.session.commit()


        return jsonify(inventory_item), 200

    except NotFound:
        return {"msg": "product not found!"}, 404
    except KeyError as err:
        return jsonify(err.args[0]), 400
    except TypeError as err:
        return jsonify(err.args[0]), 400


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

