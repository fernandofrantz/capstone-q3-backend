from werkzeug.exceptions import Forbidden

from app.configs.database import db
from app.models.customers_model import CustomerModel


def check_if_employee(identity):
    customer = db.session.query(CustomerModel).get(identity.get('id'))
    if not customer.employee:
        raise Forbidden(description="Access denied")