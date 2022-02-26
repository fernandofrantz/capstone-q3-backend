from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class CustomerModel(db.Model):
    __tablename__ = "customers"

    id: int
    name: str
    email: str
    password_hash: str
    employee: bool

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    employee = Column(Boolean, nullable=True)

    def serializer(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash
        }

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
