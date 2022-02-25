from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Boolean

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "customers"

    id: int
    name: str
    email: str
    password_hash: str
    employee: bool

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    employee = Column(Boolean, nullable=True)