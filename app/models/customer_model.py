from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Boolean, null

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "customer"

    customer_id: int
    name: str
    e_mail: str
    password_hash: str
    employee: bool

    customer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    e_mail = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    employee = Column(Boolean, nullable=True)