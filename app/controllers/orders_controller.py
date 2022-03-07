from flask import jsonify, request
from app.configs.database import db
from app.models.inventory_model import InventoryModel
from app.models.orders_model import OrderModel
from app.models.products_model import ProductModel
from app.models.orders_products_model import orders_products
from sqlalchemy import update,select
from werkzeug.exceptions import NotFound
from http import HTTPStatus
def create_order():
    default_keys=['order','customer_id']
    data=request.get_json()
    if set(data)!=set(default_keys):
        return jsonify({'error':'Wrong Keys','correct_keys':default_keys,'recived_keys':[keys for keys in data.keys()]})
    products_data=data['order']
    customer_id=data['customer_id']
    order=OrderModel(**{"customer_id":customer_id,'status':'Active'})
    for product in products_data:
        try:
            if type(product['id']) is not int:
                return jsonify({'error':f'the id must be a valid integer'}),HTTPStatus.BAD_REQUEST
            aux=ProductModel.query.get_or_404(product['id'],description={'error':f'id:{product["id"]} NOT FOUND'})
            inventory=InventoryModel.query.filter_by(product_id=product['id']).first_or_404(description=f'id:{product["id"]} NOT FOUND')
        except NotFound as e:
            return jsonify(e.description),HTTPStatus.NOT_FOUND
        if inventory.quantity <product['qtd']:
            return {'error':f'{aux.name} It unavailable'},HTTPStatus.INSUFFICIENT_STORAGE
        cost=inventory.value/inventory.quantity
        inventory.quantity-=product['qtd']
        aux.orders.append(order)
        db.session.add(order)
        db.session.commit()
        query=(update(orders_products).where(orders_products.c.order_id==order.id).values(quantity=product['qtd'],price=cost+(cost*0.2),cost=cost))
        query_order_products=select(orders_products.c.quantity,orders_products.c.price,orders_products.c.cost).where(orders_products.c.order_id==order.id)
        db.session.execute(query)
        orders_products_infos=db.session.execute(query_order_products).fetchone()
        db.session.commit()
    return jsonify({'id':order.id,
                    'order_date':order.order_date,
                    'quantity':list(orders_products_infos)[0],
                    'status':order.status,
                    'price':round(list(orders_products_infos)[1],2),
                    'cost':round(list(orders_products_infos)[2],2),
                    'products':[x for x in order.products]}),201

def get_orders():
    return jsonify(OrderModel.query.all()), 200

def get_order_by_id(order_id):
    try:
        order=OrderModel.query.get_or_404(order_id,description={'error':f'id:{order_id} NOT FOUND'})
    except NotFound as e:
        return jsonify(e.description),HTTPStatus.NOT_FOUND
    query_order_products=select(orders_products.c.quantity,orders_products.c.price,orders_products.c.cost).where(orders_products.c.order_id==order.id)
    orders_products_infos=db.session.execute(query_order_products).fetchone()
    return jsonify({'id':order.id,
                    'order_date':order.order_date,
                    'quantity':list(orders_products_infos)[0],
                    'status':order.status,
                    'price':round(list(orders_products_infos)[1],2),
                    'cost':round(list(orders_products_infos)[2],2),
                    'products':[x for x in order.products]}),201

def patch_product(order_id):
    default_keys=['quantity','price','cost','status']
    default_status=['Active','Complete','Deleted']
    data=request.get_json()
    if not set(data.keys()).issubset(set(default_keys)):
        return jsonify({'error':'Wrong Keys','valid_keys':default_keys,'recived_keys':list(data.keys())}),HTTPStatus.BAD_REQUEST
    try:
        if not (data['status']):
            for key,value in data.items():
                dict_values={key:value}
                query_select_quantity=select(orders_products.c.quantity,orders_products.c.price,orders_products.c.cost).where(orders_products.c.order_id==order_id)
                order_infos=db.session.execute(query_select_quantity).fetchone()
                query_order=(update(orders_products).where(orders_products.c.order_id==order_id).values(dict_values).returning(orders_products.c.order_id,orders_products.c.product_id,orders_products))
                order_products=db.session.execute(query_order).fetchone()
                order=OrderModel.query.get_or_404(order_id,description={'error':f'id:{order_id} NOT FOUND'})
                if order_products==None:
                    raise NotFound(description={'error':f'id:{order_id} NOT FOUND'})
                if key=='quantity':
                    inventory=InventoryModel.query.filter_by(product_id=list(order_products)[1]).first_or_404(description={'error':f'product_id:{list(order_products)[1]} NOT FOUND'})
                    inventory.quantity+=list(order_infos)[0]
                    if(inventory.quantity<value):
                        return {'error':f'product It unavailable'},HTTPStatus.INSUFFICIENT_STORAGE
                    inventory.quantity-=value
        else:
            order=OrderModel.query.get_or_404(order_id,description={'error':f'id:{order_id} NOT FOUND'})
            if not(data['status'] in default_status):
                return jsonify({'error':'The reported status is invalid'})
            order.status=data['status']
            db.session.add(order)
            db.session.commit()
            return jsonify({'msg':f'The order status has been changed to {data["status"]}'})
    except NotFound as e:
        return jsonify(e.description),HTTPStatus.NOT_FOUND
    db.session.commit()
    return jsonify({'id':order.id,
                    'order_date':order.order_date,
                    'quantity':list(order_infos)[0],
                    'status':order.status,
                    'price':round(list(order_infos)[1],2),
                    'cost':round(list(order_infos)[2],2),
                    'products':[x for x in order.products]}),201

def delete_product(order_id):
    try:
        order=OrderModel.query.get_or_404(order_id,description={'error':f'product_id:{order_id} NOT FOUND'})
    except NotFound as e:
        return jsonify(e.description)
    order.status='Deleted'
    db.session.add(order)
    db.session.commit()
    return jsonify({'msg':'Change status to Deleted'})
