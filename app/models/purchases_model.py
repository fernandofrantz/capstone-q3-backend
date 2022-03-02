from dataclasses import dataclass
import string
from app.configs.database import db
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.models.products_model import ProductModel
from app.models.purchases_products_model import purchases_products

@dataclass
class PurchaseModel(db.Model):
    __tablename__ = "purchases"

    id: int
    date: string
    products: ProductModel

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=func.current_timestamp())
    
    products = db.relationship("ProductModel", secondary=purchases_products, backref="purchases")