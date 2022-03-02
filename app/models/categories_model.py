from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String

@dataclass
class CategoryModel(db.Model):
    __tablename__ = "categories"

    id: int
    name: str
    description: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
