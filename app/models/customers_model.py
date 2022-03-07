from dataclasses import dataclass
from sqlalchemy.orm import validates
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from app.services.exceptions import ErrorCustomerValue

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "customers"

    id: int
    name: str
    email: str

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    employee = Column(Boolean, nullable=False, default=False)

    def serializer(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, str(password_to_compare))

    @validates("name", "email", "employee")
    def validates(self, key, value):
        
        if (key == "name" and type(value) != str):
            raise ErrorCustomerValue("The key name just accept string values")

        if (key == "email" and type(value) != str):
            raise ErrorCustomerValue("The key email just accept string values")

        if (key == "email" and type(value) == str):
            if(len(value.split('@')) != 2):
                raise ErrorCustomerValue("Invalid email, correct format example: johndoe@email.wathever")
        
        if  (key == 'employee' and type(value) != bool):
            raise ErrorCustomerValue("Key employee just accept boolean values")

        if (type(value) == bool and key != "employee"):
            raise ErrorCustomerValue("Key for boolean value must be 'employee'")

        return value