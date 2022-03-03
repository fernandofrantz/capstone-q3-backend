from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Float, Integer

@dataclass
class InventoryModel(db.Model):
    __tablename__ = "inventory"

    id: int
    value: int
    quantity: int
    product_id: int

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)