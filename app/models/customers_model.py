from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates
from app.configs.database import db
from dataclasses import dataclass
import re

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

    @validates("name", "password")
    def validates_user_data(self, key, value):
        if (type(value) != str):
            raise TypeError(f'key {key} recieved a {type(value).__name__}, but was expecting str')
        return value

    @validates("email")
    def validates_email(self, key, value):
        if not re.search(".{1,}@.{1,}\..{1,}", value):
            raise ValueError("wrong email format, valid example: johndoe@example.wathever")
        return value