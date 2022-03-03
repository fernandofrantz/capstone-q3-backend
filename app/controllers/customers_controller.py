from flask import current_app, jsonify, request
from app.models.customers_model import CustomerModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token

def sign_up():
    new_user_data = request.get_json()

    password_to_hash = new_user_data.pop("password")

    new_user = CustomerModel(**new_user_data)

    new_user.password = password_to_hash

    current_app.db.session.add(new_user)
    current_app.db.session.commit()

    return jsonify(new_user.serializer()), HTTPStatus.CREATED


def sign_in():
    login_data = request.get_json()

    found_user = CustomerModel.query.filter(CustomerModel.email == login_data['email']).first()

    if not found_user:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND

    if (found_user.verify_password(login_data['password'])):

        access_token = create_access_token(identity=found_user.serializer())

        return {"api_key": access_token}, HTTPStatus.OK

    else:
        return {"message": "wrong password"}, HTTPStatus.BAD_GATEWAY
