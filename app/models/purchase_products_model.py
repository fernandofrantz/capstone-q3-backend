from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from datetime import date

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "purchase_products"

    id: int
    cost: int
    quantity: int
    product_id: int
    date: str

    id = Column(Integer, primary_key=True)
    cost = Column(Integer, nullable=False)
    quantity = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=date.today())
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
