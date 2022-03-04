from flask import current_app, jsonify, request
from app.models.customers_model import CustomerModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from sqlalchemy.exc import IntegrityError

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
        return {"invalid_keys": [
            {"sent_keys": 
                list(new_user_data.keys())
            }, 
            {"valid_keys": 
                list(valid_keys.keys())
            }
        ]}, HTTPStatus.BAD_REQUEST

    except ValueError as error:
        return {"error": str(error)}, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"conflict": "email already registered"}, HTTPStatus.CONFLICT

def sign_in():
    try:    
        login_data = request.get_json()

        verify_email = login_data['email']
        verify_password = login_data['password']

        found_user = CustomerModel.query.filter(CustomerModel.email == login_data['email']).first()

        if not found_user:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND

        if (found_user.verify_password(login_data['password'])):

            access_token = create_access_token(identity=found_user.serializer())

            return {"api_key": access_token}, HTTPStatus.OK

        else:
            return {"message": "wrong password"}, HTTPStatus.BAD_GATEWAY
    
    except KeyError:
        valid_keys = {"email": str, "password": str}
        return {"invalid_keys": [
            {"sent_keys": 
                list(login_data.keys())
            }, 
            {"valid_keys": 
                list(valid_keys.keys())
            }
        ]}, HTTPStatus.BAD_REQUEST
