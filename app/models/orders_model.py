from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.orders_products_model import orders_products

@dataclass
class OrderModel(db.Model):
    __tablename__ = "orders"

    id: int
    customer_id: int
    order_date: str
    discount: int
    products: list

    id = Column(Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.now)
    discount = Column(String, nullable=True)

    products = db.relationship("ProductModel", secondary=orders_products, backref="orders")