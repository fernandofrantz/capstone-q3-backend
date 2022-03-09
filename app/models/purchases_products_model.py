from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import validates
from werkzeug.exceptions import BadRequest


@dataclass
class PurchaseProductModel(db.Model):
    __tablename__ = 'purchases_products'

    product_id: int
    quantity: int
    value: float

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchases.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)

    @validates('quantity', 'value')
    def validation(self, key, value):
        if (key == 'quantity' and type(value) != int):
            raise BadRequest(description=f"expected quantity to be: int, instead got: {type(value).__name__}")

        if (key == 'value' and type(value) != float and type(value) != int):
            raise BadRequest(description=f"expected quantity to be: int, instead got: {type(value).__name__}")

        return value