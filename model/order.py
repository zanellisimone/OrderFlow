from typing import Iterator
from model import OrderLine, OrderStatus, Client, Product
from descriptors import OrderID
from datetime import datetime
from exceptions import (
    OrderNotModificableError, 
    ProductNotFoundError,
    OrderCantBeShippedError,
    OrderCantBeConfirmedError,
    OrderCantBeCancelledError,
    EmptyOrderError
)

class Order:

    id_order = OrderID()

    def __init__(self, id_order:str, client:Client, creation_date : datetime | None = None, status : OrderStatus = OrderStatus.DRAFT, lines : list[OrderLine] | None = None) -> None:
        if not isinstance(client, Client):
            raise TypeError("The argument client must be an instance of class Client!")
        
        self.id_order = id_order
        self.__client = client
        self.__creation_date = datetime.today() if creation_date is None else creation_date
        self.__lines : list[OrderLine] = [] if lines is None else lines
        self.__status = status

    def __len__(self) -> int:
        return len(self.__lines)

    def __iter__(self) -> Iterator[OrderLine]:
        return iter(self.__lines)

    def __contains__(self, item : OrderLine) -> bool:
        if not isinstance(item, OrderLine):
            return False
        return item in self.__lines

    def __eq__(self, other_object : object) -> bool:
        if not isinstance(other_object, Order):
            return NotImplemented
        return self.id_order == other_object.id_order

    def __repr__(self) -> str:
        response = ""
        response += f"Order(id_order={self.id_order!r}, "
        response += f"client={self.__client!r}, "
        response += f"creation_date={self.__creation_date.strftime('%d/%m/%Y')!r}, "
        response += f"lines={len(self.__lines)}, "
        response += f"status={self.__status.name!r})"
        return response

    def __str__(self) -> str:
        response = ""
        response += f"ID: {self.id_order}\n"
        response += f"Client: {self.__client.id_client}\n"
        response += f"Creation date: {self.__creation_date.strftime('%d/%m/%Y')}\n"
        response += f"Lines: {len(self.__lines)}\n"
        response += f"Status: {self.__status.name}"
        return response

    def add_product(self, product : Product, quantity : int, unit_price : float | None = None) -> None:
        if self.__status != OrderStatus.DRAFT:
            raise OrderNotModificableError()
        if not isinstance(product, Product):
            raise TypeError("The argument product must be an instance of class Product!")
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("The argument quantity must be an integer!")
        if quantity <= 0:
            raise ValueError("The quantity must be positive!")
        for line in self.__lines:
            if product == line.product:
                line.quantity += quantity
                return 
        self.__lines.append(OrderLine(product, quantity, unit_price))
        
    def remove_product(self, product : Product) -> None:
        if self.__status != OrderStatus.DRAFT:
            raise OrderNotModificableError()
        if not isinstance(product, Product):
            raise TypeError("The argument product must be an instance of class Product!")
        for line in self.__lines:
            if product == line.product:
                self.__lines.remove(line)
                return
        raise ProductNotFoundError()

    def add_loaded_line(self, line: OrderLine) -> None:
        if not isinstance(line, OrderLine):
            raise TypeError("The argument must be an instance of OrderLine class!")
        if any(existing_line.product == line.product for existing_line in self.__lines):
            raise ValueError("Product already exists in the order!")
        self.__lines.append(line)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__lines)

    def confirm(self) -> None:
        if self.__status != OrderStatus.DRAFT:
            raise OrderCantBeConfirmedError()
        if not self.__lines:
            raise EmptyOrderError()
        self.__status = OrderStatus.CONFIRMED

    def ship(self) -> None:
        if self.__status != OrderStatus.CONFIRMED:
            raise OrderCantBeShippedError()
        self.__status = OrderStatus.SHIPPED

    def cancel(self) -> None:
        if self.__status not in (OrderStatus.DRAFT, OrderStatus.CONFIRMED):
            raise OrderCantBeCancelledError()
        self.__status = OrderStatus.CANCELLED

    def has_product(self, product : Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError("The argument product must be an instance of Product!")
        return any(product == order_line.product for order_line in self.__lines)

    @property
    def client(self) -> Client:
        return self.__client

    @property
    def creation_date(self) -> datetime:
        return self.__creation_date

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__lines)

    @property
    def status(self) -> OrderStatus:
        return self.__status