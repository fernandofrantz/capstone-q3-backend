from flask import request, current_app, jsonify
from app.models import InventoryModel, CustomerModel
from werkzeug.exceptions import NotFound
from app.services.validations import check_valid_patch
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def get_inventory():
    user_identity = get_jwt_identity()
    if not CustomerModel.query.get(user_identity.get('id')).employee:
        return {"msg": "Unauthorized"}, 401
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 15))
    start = (page - 1) * per_page if page > 0 else 0
    end = per_page + start
    inventory = InventoryModel.query.order_by(InventoryModel.id).all()[start:end]
    return jsonify({"page": page, "per_page": per_page, "data": inventory}), 200

@jwt_required()
def get_inventory_by_id(inventory_id):
    user_identity = get_jwt_identity()
    if not CustomerModel.query.get(user_identity.get('id')).employee:
        return {"msg": "Unauthorized"}, 401
    try:
        inventory_item = InventoryModel.query.get_or_404(inventory_id)
        return jsonify(inventory_item), 200
    except NotFound:
        return {"msg": f"Product id {inventory_id} not found."}, 404

@jwt_required()
def patch_inventory(inventory_id):
    user_identity = get_jwt_identity()
    if not CustomerModel.query.get(user_identity.get('id')).employee:
        return {"msg": "Unauthorized"}, 401
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
        return {"msg": f"Product id {inventory_id} not found."}, 404
    except KeyError as err:
        return jsonify(err.args[0]), 400
    except TypeError as err:
        return jsonify(err.args[0]), 400


@jwt_required()
def delete_inventory(inventory_id):
    user_identity = get_jwt_identity()
    if not CustomerModel.query.get(user_identity.get('id')).employee:
        return {"msg": "Unauthorized"}, 401
    try:
        inventory_item = InventoryModel.query.get_or_404(inventory_id)
        setattr(inventory_item, "value", 0)
        setattr(inventory_item, "quantity", 0)
        current_app.db.session.add(inventory_item)
        current_app.db.session.commit()
        
        return jsonify(inventory_item), 200

    except NotFound:
        return {"msg": f"Product id {inventory_id} not found."}, 404

