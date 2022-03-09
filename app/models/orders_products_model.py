from app.configs.database import db
from sqlalchemy import ARRAY,Integer

orders_products = db.Table('orders_products',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('quantity',db.Integer),
    db.Column('price',db.Float),
    db.Column('cost',db.Float),
    db.Column('quantity_per_product',ARRAY(Integer)),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'))
)