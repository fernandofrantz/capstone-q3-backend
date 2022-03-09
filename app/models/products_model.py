from dataclasses import dataclass
from sqlalchemy.orm import validates
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float

@dataclass
class ProductModel(db.Model):
    __tablename__ = "products"

    id: int
    name: str
    price: float
    category_id: int
    description: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    description = Column(String, nullable=False)

    @validates("name", "description")
    def validates_product_str_data(self, key, value):
        if (type(value) != str):
            raise TypeError(f'expected {key} to be: str, instead got: {type(value).__name__}')
        return value.lower()
    
    @validates("category_id")
    def validates_product_int_data(self, key, value):
        if (type(value) != int):
            raise TypeError(f'expected {key} to be: int, instead got: {type(value).__name__}')
        return value

    @validates("price")
    def validates_product_float_data(self, key, value):
        if (type(value) != float) and (type(value) != int):
            raise TypeError(f'expected {key} to be: float, instead got: {type(value).__name__}')
        return value