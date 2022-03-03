from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from app.models.products_model import ProductModel
from app.models.inventory_model import InventoryModel

@dataclass
class PurchaseModel(db.Model):
    __tablename__ = "purchases"

    id: int
    date: str
    products: list

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    products = db.relationship("PurchaseProductModel")

    @staticmethod
    def get_product(product_id: int) -> ProductModel:
        base_query = db.session.query(ProductModel)
        return base_query.get_or_404(product_id)

    @staticmethod
    def get_inventory(product_id: int) -> InventoryModel:
        base_query = db.session.query(InventoryModel)
        return base_query.filter_by(product_id=product_id).first_or_404()