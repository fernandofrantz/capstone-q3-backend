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

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    employee = Column(Boolean, nullable=False, default=False)
    password_hash = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)

    