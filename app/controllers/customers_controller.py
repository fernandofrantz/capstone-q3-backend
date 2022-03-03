from flask import current_app, jsonify, request
from app.models.customers_model import CustomerModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from sqlalchemy.exc import IntegrityError
from app.services.exceptions import ErrorCustomerValue

def sign_up():
   try:
      new_user_data = request.get_json()

      password_to_hash = new_user_data.pop("password")

      new_user = CustomerModel(**new_user_data)

      new_user.password = str(password_to_hash)

      current_app.db.session.add(new_user)
      current_app.db.session.commit()

      return jsonify(new_user.serializer()), HTTPStatus.CREATED

   except ErrorCustomerValue as error:
      return {"message": str(error)}, HTTPStatus.BAD_REQUEST

   except IntegrityError:
      return {"message": "email already registered"}

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
