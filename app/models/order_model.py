from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, null
import datetime

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "order"

    order_id: int
    customer_order_id: int
    order_date: str
    discount: int

    order_id = Column(Integer, primary_key=True)
    customer_order_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    order_date = Column(Date, nullable=False, default=datetime.now())
    discount = Column(String, nullable=True)