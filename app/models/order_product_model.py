from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, null
import datetime

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "order_product"

    order_product_id: int
    order_id: int
    product_id: str
    quantity: int
    price: int
    cost: int

    order_product_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
