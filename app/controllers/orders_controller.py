from flask import jsonify, request
from app.configs.database import db
from app.models.customers_model import CustomerModel
from app.models.inventory_model import InventoryModel
from app.models.orders_model import OrderModel
from app.models.products_model import ProductModel
from app.models.orders_products_model import orders_products
from sqlalchemy import update,select
from werkzeug.exceptions import NotFound,BadRequestKeyError
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity

from app.services.pagination_services import serialize_pagination
@jwt_required()
def create_order():
    customer=get_jwt_identity()
    default_keys=['order']
    default_keys_product=['id','quantity']
    data=request.get_json()
    if set(data)!=set(default_keys):
        return jsonify({'valid_keys':default_keys,'recieved_keys':[keys for keys in data.keys()]})
    products_data=data['order']
    customer_id=customer['id']
    try:
        customer=CustomerModel.query.get_or_404(customer['id'],description={'msg':f'customer id {customer["id"]} not found'})
    except NotFound as e:
        return jsonify(e.description),HTTPStatus.NOT_FOUND
    try:
        order=OrderModel(**{"customer_id":customer_id,'status':'Active'})
    except BadRequestKeyError as e:
        return jsonify(e.description),HTTPStatus.BAD_REQUEST
    quantity_total=0
    total=0
    for product in products_data:
        try:
            if set(default_keys_product)!=set(list(product.keys())):
                return jsonify({'required_keys':default_keys_product,'recieved_keys':[keys for keys in product.keys()]})
            if type(product['id']) is not int or type(product['quantity']) is not int:
                return jsonify({'msg':f'id or quantity is not int'}),HTTPStatus.BAD_REQUEST
            if not (product['quantity']>0):
                return jsonify({'msg':f'product id {product["id"]} is not available'})
            aux=ProductModel.query.get_or_404(product['id'],description={'msg':f'product id {product["id"]} not found'})
            inventory=InventoryModel.query.filter_by(product_id=product['id']).first_or_404(description=f'product id {product["id"]} not found')
        except NotFound as e:
            return jsonify(e.description),HTTPStatus.NOT_FOUND
        if inventory.quantity <product['quantity']:
            return {'msg':f'product id {aux.id} is not available'},HTTPStatus.INSUFFICIENT_STORAGE
        cost=inventory.value/inventory.quantity
        inventory.quantity-=product['quantity']
        inventory.value-=cost*product['quantity']
        db.session.add(order)
        aux.orders.append(order)
        db.session.commit()
        quantity_total+=product['quantity']
        total+=aux.price*product['quantity']
        query_order_products=select(orders_products.c.id).order_by(orders_products.c.id.desc())
        last_id=db.session.execute(query_order_products).first()
        query=(update(orders_products).where(orders_products.c.id==last_id[0]).values(quantity=product['quantity'],price=aux.price,cost=round(cost,2)))
        db.session.execute(query)
        db.session.commit()
    return jsonify({'id':order.id,
                    'name':customer.name,
                    'order_date':order.order_date,
                    'quantity':quantity_total,
                    'status':order.status,
                    'total':round(total,2),
                    'products':[x for x in order.products]}),201
@jwt_required()
def get_orders():
    try:
        user_identity = get_jwt_identity()
        if not CustomerModel.query.get(user_identity.get('id')).employee:
            return {"msg": "access denied"}, 403
        page=request.args.get("page",type=int)
        per_page=request.args.get("per_page",type=int)
        print(per_page)
        if not page:
            page=1
        if not per_page:
            per_page=3
        data=OrderModel.query.order_by(OrderModel.id).paginate(page, per_page)
        response = serialize_pagination(data, "orders")
        return jsonify(response), 200

    except NotFound:
        return jsonify({"msg": "page not found"}), HTTPStatus.NOT_FOUND
    
@jwt_required()
def get_order_by_id(order_id):
    user_identity = get_jwt_identity()
    try:
        order=OrderModel.query.get_or_404(order_id,description={'msg':f'id:{order_id} NOT FOUND'})
    except NotFound as e:
        return jsonify(e.description),HTTPStatus.NOT_FOUND
    if not (CustomerModel.query.get(user_identity.get('id')).employee) and (order.customer_id!=user_identity.get('id')):
        return {"msg": "access denied"}, 403
    
    query_order_products=select(orders_products.c.quantity,orders_products.c.price,orders_products.c.cost).where(orders_products.c.order_id==order.id)
    orders_products_infos=db.session.execute(query_order_products).all()
    total=0
    quantity_total=0
    for infos in orders_products_infos:
        quantity_total+=infos[0]
        total+=infos[0]*infos[1]
    return jsonify({'id':order.id,
                    'order_date':order.order_date,
                    'quantity':quantity_total,
                    'status':order.status,
                    'total':round(total,2),
                    'products':[x for x in order.products]}),201
@jwt_required()
def patch_product(order_id):
    user_identity = get_jwt_identity()
    default_keys=['products','status']
    default_status=['active','complete']
    data=request.get_json()
    if not set(data.keys()).issubset(set(default_keys)):
        return jsonify({'valid_keys':default_keys,'recieved_keys':list(data.keys())}),HTTPStatus.BAD_REQUEST
    query_select_quantity=select(orders_products.c.id,orders_products.c.product_id,orders_products.c.quantity,orders_products.c.price,orders_products.c.cost).where(orders_products.c.order_id==order_id).order_by(orders_products.c.id)
    query_select_id=select(orders_products.c.product_id).where(orders_products.c.order_id==order_id).order_by(orders_products.c.id)
    execute_id=db.session.execute(query_select_id).all()
    execute_id=[x[0] for x in execute_id]
    id_data=[product['id'] for product in data.get('products', [])]
    if not (set(id_data).issubset(execute_id)):
        error_id=set(id_data)-set(execute_id)
        return jsonify({'msg':f'products id {list(error_id)} invalids'})
    total=0
    quantity_total=0
    try:
        order=OrderModel.query.get_or_404(order_id,description={'msg':f'id:{order_id} NOT FOUND'})
        if not (CustomerModel.query.get(user_identity.get('id')).employee) and (order.customer_id!=user_identity.get('id')):
            return {"msg": "access denied"}, 403
        if order.status=='deleted':
            return jsonify({'msg':'order already deleted.'})
        if (data.get('products')):
            order_infos=db.session.execute(query_select_quantity).all()
            for infos in order_infos:
                for product in sorted(data['products'], key=lambda k: k['id']):
                    if infos[1]==product['id']:
                        if not (product.get('id')) or not (product.get('quantity')):
                            return jsonify({'msg':'id or quantity not informed'}),HTTPStatus.BAD_REQUEST
                        if  type(product['id']) is not int  or type(product['quantity']) is not int:
                            return jsonify({'msg':'id or quantity is not int'}),HTTPStatus.BAD_REQUEST
                        dict_values={'quantity':product['quantity']}
                        query_order=(update(orders_products).where(orders_products.c.id==infos[0]).values(dict_values))
                        db.session.execute(query_order)
                        inventory=InventoryModel.query.filter_by(product_id=product['id']).first_or_404(description={'msg':f'product_id:{product["id"]} NOT FOUND'})
                        # inventory.quantity+=infos[2]
                        # inventory.value+=infos[4]
                        if(inventory.quantity<(product['quantity']-infos[2])) or inventory.quantity == 0:
                            return {'msg':f'product It unavailable'},HTTPStatus.INSUFFICIENT_STORAGE
                        cost=inventory.value/inventory.quantity
                        inventory.value+=(cost*(infos[2]-product['quantity']))
                        inventory.quantity-=product['quantity']-infos[2]
                db.session.commit()
        if data.get('status'):

            if not(data['status'].lower() in default_status):
                return jsonify({'msg':'invalid status, valid patch status: active, complete'}),HTTPStatus.BAD_REQUEST
            order.status=data['status'].lower()
            db.session.add(order)
            db.session.commit()
    except NotFound as e:
        return jsonify(e.description),HTTPStatus.NOT_FOUND
    order_infos=db.session.execute(query_select_quantity).all()
    for infos in  order_infos:
        quantity_total+=infos[2]
        total+=infos[2]*round(infos[3],2)
    db.session.commit()
    return jsonify({'id':order.id,
                    'order_date':order.order_date,
                    'quantity':quantity_total,
                    'status':order.status,
                    'total':round(total,2),
                    'products':[x for x in order.products]}),201
@jwt_required()
def delete_product(order_id):
    user_identity = get_jwt_identity()
    try:
        order=OrderModel.query.get_or_404(order_id,description={'msg':f'order id {order_id} not found'})
        if not (CustomerModel.query.get(user_identity.get('id')).employee) and (order.customer_id!=user_identity.get('id')):
            return {"msg": "access denied"}, 403
    except NotFound as e:
        return jsonify(e.description)
    query_select_quantity=select(orders_products.c.id,orders_products.c.product_id,orders_products.c.quantity,orders_products.c.price,orders_products.c.cost).where(orders_products.c.order_id==order_id).order_by(orders_products.c.id)
    order_infos=db.session.execute(query_select_quantity).all()
    for infos in order_infos:
        inventory=InventoryModel.query.filter_by(product_id=infos[1]).first_or_404(description={'msg':f'product_id:{infos[1]} NOT FOUND'})
        inventory.quantity+=infos[2]
        inventory.value+=infos[4]
    order.status='deleted'
    db.session.add(order)
    db.session.commit()
    return jsonify({'msg':'order deleted'})
