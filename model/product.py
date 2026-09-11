from __future__ import annotations
from descriptors import ProductID, StringNotEmpty, PositiveNumber, NonNegativeInteger

class Product:

    id_product = ProductID()
    name = StringNotEmpty()
    category = StringNotEmpty()
    price = PositiveNumber()
    quantity_available = NonNegativeInteger()

    def __init__(self, id_product:str, name:str, category:str, price:float | int, quantity_available:int) -> None:
        self.id_product = id_product
        self.name = name
        self.category = category
        self.price = price
        self.quantity_available = quantity_available

    def __repr__(self) -> str:
        return f"Product(id_product={self.id_product!r}, name={self.name!r}, category={self.category!r}, price={self.price!r}, quantity_available={self.quantity_available!r})"

    def __str__(self) -> str:
        response = ""
        response += f"ID: {self.id_product}\n"
        response += f"Name: {self.name}\n"
        response += f"Category: {self.category}\n"
        response += f"Price: {self.price:.2f}\n"
        response += f"Quantity available: {self.quantity_available}"
        return response

    def __eq__(self, other_object:object) -> bool:
        if not isinstance(other_object, Product):
            return NotImplemented
        return self.id_product == other_object.id_product

    def __hash__(self) -> int:
        return hash(self.id_product)