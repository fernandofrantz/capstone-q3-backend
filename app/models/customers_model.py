from dataclasses import dataclass
from sqlalchemy.orm import validates
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
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

    @validates("name", "email", "password")
    def validates(self, key, value):
        
        if (key == "email"):
            r = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
            if r.match(value):
                pass
            else:
                raise ValueError("wrong email format, valid example: johndoe@example.wathever")

        if (key != "name" and key != "email" and key != "password"):
            raise KeyError

        if (type(value) != str):
            raise ValueError(f'key {key} recieved a {type(value).__name__}, but was expecting str')

        return value



        # # def alphanumeric(password):
        #     if password == '':
        #         return False
        #     return False if re.search("[^\u00C0-\u017FA-Za-z0-9]", password) else True