from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import validates
from datetime import datetime
from app.models.orders_products_model import orders_products
from werkzeug.exceptions import BadRequestKeyError
@dataclass
class OrderModel(db.Model):
    __tablename__ = "orders"

    id: int
    order_date: str
    products:list

    id = Column(Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now)
    discount = Column(String, nullable=True)
    status=Column(String,nullable=False)

    products = db.relationship("ProductModel", secondary=orders_products, backref="orders")
    @validates('customer_id')
    def validate_customer_id(self,key,value):
        if key=='customer_id' and type(value) is not int:
            raise BadRequestKeyError(description={'error':f'expected customer_id to be: int, instead got: {type(value).__name__}'})
        return value