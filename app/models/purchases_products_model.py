from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Float, Integer, ForeignKey


@dataclass
class PurchaseProductModel(db.Model):
    __tablename__ = "purchases_products"

    product_id: int
    quantity: int
    value: float

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchases.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)