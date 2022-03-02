from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.products_model import ProductModel
from app.models.orders_products_model import orders_products

@dataclass
class OrderModel(db.Model):
    __tablename__ = "orders"

    id: int
    customer_id: int
    order_date: str
    discount: int
    products: ProductModel

    id = Column(Integer, primary_key=True)
    discount = Column(String, nullable=True)
    order_date = Column(DateTime, nullable=False, default=func.current_timestamp())
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    products = db.relationship("ProductModel", secondary=orders_products, backref="orders")