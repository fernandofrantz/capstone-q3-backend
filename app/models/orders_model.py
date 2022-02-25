from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from datetime import date

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "orders"

    id: int
    customer_id: int
    order_date: str
    discount: int

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(Date, nullable=False, default=date.today())
    discount = Column(String, nullable=True)