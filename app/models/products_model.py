from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String

@dataclass
class ProductModel(db.Model):
    __tablename__ = "products"

    id: int
    name: str
    price: str
    category_id: int
    description: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    description = Column(String, nullable=False)