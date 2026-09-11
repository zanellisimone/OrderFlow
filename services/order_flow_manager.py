from model import Client, Order, Product, OrderStatus
from exceptions import (
    ClientNotFoundError,
    ClientHasOrdersError,
    ClientAlreadyExistsError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductHasOrdersError,
    OrderAlreadyExistsError,
    OrderNotFoundError,
    EmptyOrderError,
    InsufficientStockError
)

class OrderFlowManager:
    def __init__(self) -> None:
        self.__clients : dict[str, Client] = {}
        self.__products : dict[str, Product] = {}
        self.__orders : dict[str, Order] = {}

    def add_client(self, new_client : Client) -> None:
        if not isinstance(new_client, Client):
            raise TypeError("The new client must be an instance of class Client!")
        if new_client.id_client in self.__clients:
            raise ClientAlreadyExistsError()
        self.__clients[new_client.id_client] = new_client

    def get_client(self, id_client : str) -> Client:
        if not isinstance(id_client, str):
            raise TypeError("The id of the client must be a string!")
        id_client = id_client.strip().upper()
        client = self.__clients.get(id_client)
        if client is None:
            raise ClientNotFoundError()
        return client

    def remove_client(self, id_client : str) -> None:
        client = self.get_client(id_client)
        if any(client == order.client for order in self.__orders.values()):
            raise ClientHasOrdersError()
        self.__clients.pop(client.id_client)

    def get_clients(self) -> tuple[Client, ...]:
        return tuple(self.__clients.values())

    def add_product(self, new_product : Product) -> None:
        if not isinstance(new_product, Product):
            raise TypeError("The new product must be an instance of class Product!")
        if new_product.id_product in self.__products:
            raise ProductAlreadyExistsError()
        self.__products[new_product.id_product] = new_product

    def get_product(self, id_product : str) -> Product:
        if not isinstance(id_product, str):
            raise TypeError("The id of the product must be a string!")
        id_product = id_product.strip().upper()
        product = self.__products.get(id_product)
        if product is None:
            raise ProductNotFoundError()
        return product

    def remove_product(self, id_product : str) -> None:
        product = self.get_product(id_product)
        if any(order.has_product(product) for order in self.__orders.values()):
            raise ProductHasOrdersError()
        self.__products.pop(product.id_product)

    def get_products(self) -> tuple[Product, ...]:
        return tuple(self.__products.values())
        
    def create_order(self, id_order : str, id_client : str) -> Order:
        if not isinstance(id_order, str):
            raise TypeError("The id of the order must be a string!")
        id_order = id_order.strip().upper()
        if id_order in self.__orders:
            raise OrderAlreadyExistsError()
        client = self.get_client(id_client)
        new_order = Order(id_order, client)
        self.__orders[id_order] = new_order
        return new_order

    def add_order(self, new_order : Order) -> None:
        if not isinstance(new_order, Order):
            raise TypeError("The argument must be an instance of Order class!")
        if new_order.id_order in self.__orders:
            raise OrderAlreadyExistsError()
        self.__orders[new_order.id_order] = new_order

    def get_order(self, id_order : str) -> Order:
        if not isinstance(id_order, str):
            raise TypeError("The id of the order must be a string!")
        id_order = id_order.strip().upper()
        order = self.__orders.get(id_order)
        if order is None:
            raise OrderNotFoundError()
        return order

    def add_product_to_order(self, id_order : str, id_product : str, quantity : int) -> None:
        order = self.get_order(id_order)
        product = self.get_product(id_product)
        order.add_product(product, quantity)

    def confirm_order(self, id_order : str) -> None:
        order = self.get_order(id_order)
        for line in order.lines:
            if line.quantity > line.product.quantity_available:
                raise InsufficientStockError(line.product.name)
        order.confirm()
        for line in order.lines:
            line.product.quantity_available -= line.quantity

    def ship_order(self, id_order : str) -> None:
        self.get_order(id_order).ship()

    def cancel_order(self, id_order : str) -> None:
        order = self.get_order(id_order)
        old_status = order.status
        order.cancel()
        if old_status == OrderStatus.DRAFT:
            return
        for line in order.lines:
            line.product.quantity_available += line.quantity

    def get_orders(self) -> tuple[Order, ...]:
        return tuple(self.__orders.values())

    def get_orders_by_client(self, id_client : str) -> tuple[Order, ...]:
        client = self.get_client(id_client)
        return tuple(order for order in self.__orders.values() if order.client == client)

    def get_orders_by_status(self, status : OrderStatus) -> tuple[Order, ...]:
        if not isinstance(status, OrderStatus):
            raise TypeError("The status must be an element of OrderStatus Enum!")
        return tuple(order for order in self.__orders.values() if order.status == status)