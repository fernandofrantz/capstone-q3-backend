from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from app.models.products_model import ProductModel

@dataclass
class CategoryModel(db.Model):
    __tablename__ = "categories"

    id: int
    name: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    @validates('name')
    def validate_fildes(self,_,value):
        if not type(value) == str:
            raise ValueError
        return value.lower()

    def serializer(self,list_products:list[ProductModel]) -> dict:
        def format_product(product:ProductModel) -> dict:
            return  {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "description": product.description
                    }    
        products_formated = [format_product(product) for product in list_products]

        return {self.name:products_formated}

