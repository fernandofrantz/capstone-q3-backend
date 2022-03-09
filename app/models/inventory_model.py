from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import validates

@dataclass
class InventoryModel(db.Model):
    __tablename__ = "inventory"

    id: int
    value: float
    quantity: int

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    valid_inputs = {
        "value": float,
        "quantity": int
    }

    @validates("value", "quantity")
    def check_type_string(self, key, value):
        if type(value) is self.valid_inputs.get(key) or (type(value) is int and self.valid_inputs.get(key) is float):
            return value
        else:
            raise TypeError({
                "error": f"expected {key} to be: {self.valid_inputs.get(key).__name__}, instead got: {type(value).__name__}"
                })
    