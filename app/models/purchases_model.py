from dataclasses import dataclass
import string
from app.configs.database import db
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from app.models.purchases_products_model import purchases_products

@dataclass
class PurchaseModel(db.Model):
    __tablename__ = "purchases"

    id: int
    date: string
    products: list

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    products = db.relationship("ProductModel", secondary=purchases_products, backref="purchases")