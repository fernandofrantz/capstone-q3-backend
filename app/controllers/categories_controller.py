from flask import jsonify,request,current_app
from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.categories_model import CategoryModel
from app.models.products_model import ProductModel

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
        for key,value in data.items():
            if type(value) != str:
                raise TypeError
            setattr(category_filtred,key,value)
            
        session.add(category_filtred)
        session.commit()

    except TypeError:
        return {'error':'the type name is not a string'}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {'error':'this category name already exists!'},HTTPStatus.CONFLICT

    return jsonify(category_filtred),HTTPStatus.OK