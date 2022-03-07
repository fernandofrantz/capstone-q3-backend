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
            raise TypeError(f'key {key} recieved a {type(value).__name__}, but in name or description was expecting str')
        return value
    
    @validates("category_id")
    def validates_product_int_data(self, key, value):
        if (type(value) != int):
            raise TypeError(f'key {key} recieved a {type(value).__name__}, but in category_id was expecting int')
        return value

    @validates("price")
    def validates_product_float_data(self, key, value):
        if (type(value) != float):
            raise TypeError(f'key {key} recieved a {type(value).__name__}, but in price was expecting float')
        return value