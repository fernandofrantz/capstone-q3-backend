from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

@dataclass
class CategoryModel(db.Model):
    __tablename__ = "categories"

    id: int
    name: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    @validates('name')
    def validate_fildes(self,_,value):
        if not type(value)== str:
            raise ValueError
        return value
