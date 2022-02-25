from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "order_products"

    id: int
    order_id: int
    product_id: str
    quantity: int
    price: int
    cost: int

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
