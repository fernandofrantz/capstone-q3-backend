from app.services.validations import check_valid_patch
from app.models.customers_model import CustomerModel
from flask_jwt_extended import create_access_token
from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from http import HTTPStatus
import re

def sign_up():
    try:
        new_user_data = request.get_json()

        verify_name = new_user_data['name']
        verify_email = new_user_data['email']
        verify_password = new_user_data['password']

        if len(new_user_data) != 3: raise KeyError

        password_to_hash = new_user_data.pop("password")

        new_user = CustomerModel(**new_user_data)

        new_user.password = str(password_to_hash)

        current_app.db.session.add(new_user)
        current_app.db.session.commit()

        return jsonify(new_user.serializer()), HTTPStatus.CREATED

    except KeyError:
        valid_keys = {"name": str, "email": str, "password": str}
        return {
            "required_keys": 
                list(valid_keys.keys()),
            "recieved_keys": 
                list(new_user_data.keys())
        }, HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST

    except TypeError as err:
        return jsonify({"error": err.args[0]}), HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "email already registered"}, HTTPStatus.CONFLICT

def sign_in():
    try:
        login_data = request.get_json()

        verify_email = login_data['email']
        verify_password = login_data['password']

        found_user = CustomerModel.query.filter(CustomerModel.email == login_data['email']).first()

        if not found_user:
            return {"error": "user not found"}, HTTPStatus.NOT_FOUND

        if (found_user.verify_password(login_data['password'])):

            access_token = create_access_token(identity=found_user.serializer())

            return {"api_key": access_token}, HTTPStatus.OK

        else:
            return {"error": "login failed, incorrect e-mail or password"}, HTTPStatus.BAD_GATEWAY
    
    except KeyError:
        valid_keys = {"email": str, "password": str}
        return  {
            "required_keys": 
                list(valid_keys.keys()),
            "recieved_keys": 
                list(login_data.keys())
        }, HTTPStatus.BAD_REQUEST

@jwt_required()
def patch_user(user_id):
    try:
        requesting_data = request.get_json()

        user_to_patch = CustomerModel.query.filter(CustomerModel.id == user_id).first()

        valid_keys = ["name", "email"]
        check_valid_patch(requesting_data, valid_keys)
    
        patching_data = {
            "name": requesting_data.get('name'),
            "email": requesting_data.get('email')
        }

        for key, value in patching_data.items():
            if(value != None):
                setattr(user_to_patch, key, value)
                current_app.db.session.add(user_to_patch)
        current_app.db.session.commit()
        return '', HTTPStatus.OK
            
    except KeyError as error:
        return jsonify(error.args[0]), HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST