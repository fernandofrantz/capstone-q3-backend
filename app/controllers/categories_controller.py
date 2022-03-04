from flask import jsonify,request,current_app
from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.categories_model import CategoryModel
from app.models.products_model import ProductModel
from app.services.validations import check_valid_patch

def get_categories():
    all_categories = CategoryModel.query.all()
    return jsonify(all_categories), HTTPStatus.OK

def get_category_by_id(category_id:int):
    category_filtred:CategoryModel = CategoryModel.query.get(category_id)
    if not category_filtred:
        return {'error':'category not found'},HTTPStatus.NOT_FOUND
    products_filtred_by_category:list[ProductModel] = ProductModel.query.filter_by(category_id=category_id).all()
    return {category_filtred.name:products_filtred_by_category},HTTPStatus.OK

def patch_category(category_id:int):
    session:Session = current_app.db.session
    data:dict = request.get_json()
    category_filtred:CategoryModel = CategoryModel.query.get(category_id)

    if not category_filtred:
        return {'error':'category not found'},HTTPStatus.NOT_FOUND

    try:
        valid_keys = ['name']
        check_valid_patch(data,valid_keys)

        for key,value in data.items():
            setattr(category_filtred,key,value)
         
        session.add(category_filtred)
        session.commit()

    except ValueError:
        return {'error':'the type name is not a string'}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {'error':'this category name already exists!'},HTTPStatus.CONFLICT
    except KeyError as err:
        return jsonify(err.args[0]),HTTPStatus.BAD_REQUEST

    return jsonify(category_filtred),HTTPStatus.OK