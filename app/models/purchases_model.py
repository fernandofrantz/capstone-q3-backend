from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from app.models.products_model import ProductModel
from app.models.inventory_model import InventoryModel
from app.services.exceptions import (
    EmptyPurchaseProductListError as EmptyList,
    InvalidPurchaseProductFieldError as InvalidField,
    PurchaseProductNotFoundError as ProductNotFound,
    PurchaseNotFoundError as PurchaseNotFound
)


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
    def check_products_list(products_list: list) -> list:
        if len(products_list) < 1:
            raise EmptyList

        return products_list

    @staticmethod
    def get_product(product_id: int) -> ProductModel:
        if not product_id:
            raise InvalidField

        base_query = db.session.query(ProductModel)
        product = base_query.get(product_id)

        if not product:
            raise ProductNotFound(product_id)

        return product

    @staticmethod
    def get_inventory(product_id: int) -> InventoryModel:
        base_query = db.session.query(InventoryModel)
        return base_query.filter_by(product_id=product_id).first()

    @staticmethod
    def check_purchase(purchase) -> None:
        if not purchase:
            raise PurchaseNotFound