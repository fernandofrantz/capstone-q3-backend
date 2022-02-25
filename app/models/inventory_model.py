from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "inventory"

    id: int
    value: int
    quantity: int
    product_id: int

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)