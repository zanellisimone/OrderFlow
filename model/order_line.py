from __future__ import annotations
from model import Product
from descriptors import PositiveInteger, PositiveNumber

class OrderLine:

    quantity = PositiveInteger()
    unit_price = PositiveNumber()

    def __init__(self, product:Product, quantity:int, unit_price = None) -> None:
        if not isinstance(product, Product):
            raise TypeError("Argument product must be an instance of class Product!")
        self.__product = product
        self.quantity = quantity
        self.unit_price = product.price if unit_price is None else unit_price

    def __repr__(self) -> str:
        return f"OrderLine(product={self.__product!r}, quantity={self.quantity!r}, unit_price={self.unit_price!r})"

    def __str__(self) -> str:
        response = ""
        response += f"Product:\n{self.__product}\n"
        response += f"Quantity: {self.quantity}\n"
        response += f"Unit price: {self.unit_price:.2f}"
        return response

    def __eq__(self, other_object:object) -> bool:
        if not isinstance(other_object, OrderLine):
            return NotImplemented        
        return self.__product == other_object.product and self.unit_price == other_object.unit_price

    def calculate_subtotal(self) -> float:
        return self.quantity * self.unit_price

    @property
    def product(self) -> Product:
        return self.__product