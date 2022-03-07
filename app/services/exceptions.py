class ErrorCustomerValue(Exception):
    pass

class IdProductNotFoundError(Exception):
    status_code = 404
    def __init__(self, product_id):
        self.response = {"error": f"Product of id {product_id} not found"}