from flask import request, current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, Forbidden

from app.models import InventoryModel, CustomerModel
from app.services.validations import check_valid_patch
from app.services.pagination_services import serialize_pagination
from app.services.customers_services import check_if_employee


@jwt_required()
def get_inventory():
    try:
        check_if_employee(get_jwt_identity())

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 15))

        inventory = InventoryModel.query.order_by(InventoryModel.id).paginate(page, per_page)
        response = serialize_pagination(inventory, "inventory")

        return jsonify(response), 200

    except Forbidden as e:
        return jsonify({"msg": e.description}), e.code
    except NotFound:
        return jsonify({"msg": "page not found"}), HTTPStatus.NOT_FOUND

@jwt_required()
def get_inventory_by_id(inventory_id):
    try:
        check_if_employee(get_jwt_identity())

        inventory_item = InventoryModel.query.get_or_404(inventory_id)

        return jsonify(inventory_item), 200

    except Forbidden as e:
        return jsonify({"msg": e.description}), e.code
    except NotFound:
        return {"msg": f"product id {inventory_id} not found"}, HTTPStatus.NOT_FOUND

@jwt_required()
def patch_inventory(inventory_id):
    try:
        check_if_employee(get_jwt_identity())

        data = request.get_json()
        inventory_item = InventoryModel.query.get_or_404(inventory_id)

        valid_keys = ["value", "quantity"]
        check_valid_patch(data, valid_keys)

        for key, value in data.items():
            setattr(inventory_item, key, value)

        current_app.db.session.add(inventory_item)
        current_app.db.session.commit()


        return jsonify(inventory_item), HTTPStatus.OK

    except Forbidden as e:
        return jsonify({"msg": e.description}), e.code
    except NotFound:
        return {"msg": f"product id {inventory_id} not found"}, HTTPStatus.NOT_FOUND
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST
    except TypeError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_inventory(inventory_id):
    try:
        check_if_employee(get_jwt_identity())

        inventory_item = InventoryModel.query.get_or_404(inventory_id)
        setattr(inventory_item, "value", 0)
        setattr(inventory_item, "quantity", 0)
        current_app.db.session.add(inventory_item)
        current_app.db.session.commit()
        
        return jsonify(inventory_item), HTTPStatus.OK

    except Forbidden as e:
        return jsonify({"msg": e.description}), e.code
    except NotFound:
        return {"msg": f"product id {inventory_id} not found"}, HTTPStatus.NOT_FOUND

