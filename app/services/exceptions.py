class ErrorCustomerValue(Exception):
    pass

class MissingPurchaseProductsListError(Exception):
    status_code = 400
    response = {"error": "Request must contain a 'products' list"}

class EmptyPurchaseProductListError(Exception):
    status_code = 400
    response = {"error": "The 'products' list must contain at least one product"}

class InvalidPurchaseProductsListError(Exception):
    status_code = 400
    response = {"error": "The 'products' field must be a list"}

class InvalidPurchaseProductFieldError(Exception):
    status_code = 400
    response = {"error": "Product data either missing or invalid"}

class PurchaseProductNotFoundError(Exception):
    status_code = 404
    def __init__(self, product_id):
        self.response = {"error": f"Product of id {product_id} not found"}

class PurchaseNotFoundError(Exception):
    status_code = 404
    response = {"error": "Purchase not found"}
