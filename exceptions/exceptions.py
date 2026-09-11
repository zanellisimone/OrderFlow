class OrderNotModificableError(Exception):
    def __init__(self, message="The order can't be modified!"):
        super().__init__(message)

class ProductNotFoundError(Exception):
    def __init__(self, message="Product not found!"):
        super().__init__(message)

class OrderCantBeConfirmedError(Exception):
    def __init__(self, message="The order can't be confirmed!"):
        super().__init__(message)

class OrderCantBeShippedError(Exception):
    def __init__(self, message="The order can't be shipped!"):
        super().__init__(message)

class OrderCantBeCancelledError(Exception):
    def __init__(self, message="The order can't be cancelled!"):
        super().__init__(message)

class EmptyOrderError(Exception):
    def __init__(self, message="The order is empty!"):
        super().__init__(message)

class ClientAlreadyExistsError(Exception):
    def __init__(self, message="The client already exists!"):
        super().__init__(message)

class ClientNotFoundError(Exception):
    def __init__(self, message="Client not found!"):
        super().__init__(message)

class ClientHasOrdersError(Exception):
    def __init__(self, message="The client has orders, so can't be removed!"):
        super().__init__(message)

class ProductAlreadyExistsError(Exception):
    def __init__(self, message="The product already exists!"):
        super().__init__(message)

class ProductHasOrdersError(Exception):
    def __init__(self, message="The product has orders, so can't be removed!"):
        super().__init__(message)

class OrderAlreadyExistsError(Exception):
    def __init__(self, message="The order already exists!"):
        super().__init__(message)

class OrderNotFoundError(Exception):
    def __init__(self, message="Order not found!"):
        super().__init__(message)

class InsufficientStockError(Exception):
    def __init__(self, product_name : str):
        message = f"There isn't enough {product_name} for the order!"
        super().__init__(message)