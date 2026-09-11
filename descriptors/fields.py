from __future__ import annotations
from typing import overload
from datetime import datetime
import re

EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_PATTERN = r"^\+?[0-9]{8,15}$"
CLIENT_ID_PATTERN = r"^C\d{4}$"
PRODUCT_ID_PATTERN = r"^P\d{4}$"
ORDER_ID_PATTERN = r"^O\d{4}$"

class ClientID:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> ClientID:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> str:
        ...

    def __get__(self, instance: object | None, owner:type) -> str | ClientID:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:str) -> None:
        if self.name in instance.__dict__:
            raise AttributeError(f"{self.name[1:]} cannot be modified after initialization!")
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string!")
        value = value.strip().upper()
        if re.fullmatch(CLIENT_ID_PATTERN, value) is None:
            raise ValueError(f"{self.name[1:]} isn't in a correct form!")
        instance.__dict__[self.name] = value

class StringNotEmpty:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> StringNotEmpty:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> str:
        ...

    def __get__(self, instance:object | None, owner:type) -> str | StringNotEmpty:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string!")
        value = value.strip()
        if not value:
            raise ValueError(f"{self.name[1:]} mustn't be empty!")
        instance.__dict__[self.name] = value

class ValidEmail:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> ValidEmail:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> str:
        ...

    def __get__(self, instance:object | None, owner:type) -> str | ValidEmail:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string!")
        value = value.strip()
        if not value:
            raise ValueError(f"{self.name[1:]} mustn't be empty!")
        if re.fullmatch(EMAIL_PATTERN, value) is None:
            raise ValueError(f"{self.name[1:]} isn't in a correct form!")
        instance.__dict__[self.name] = value

class ValidPhoneNumber:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> ValidPhoneNumber:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> str:
        ...

    def __get__(self, instance:object | None, owner:type) -> str | ValidPhoneNumber:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:str | None) -> None:
        if value is None:
            instance.__dict__[self.name] = None
            return
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string!")
        value = value.strip()
        value = value.replace(" ", "")
        if re.fullmatch(PHONE_PATTERN, value) is None:
            raise ValueError(f"{self.name[1:]} isn't in a correct form!")
        instance.__dict__[self.name] = value

class PositiveNumber:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> PositiveNumber:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> float:
        ...

    def __get__(self, instance:object | None, owner:type) -> float | PositiveNumber:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:float | int) -> None:
        if not isinstance(value, (float, int)) or isinstance(value, bool):
            raise TypeError(f"{self.name[1:]} must be a number!")
        if value <= 0:
            raise ValueError(f"{self.name[1:]} must be positive!")
        instance.__dict__[self.name] = float(value)

class ProductID:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> ProductID:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> str:
        ...

    def __get__(self, instance: object | None, owner:type) -> str | ProductID:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:str) -> None:
        if self.name in instance.__dict__:
            raise AttributeError(f"{self.name[1:]} cannot be modified after initialization!")
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string!")
        value = value.strip().upper()
        if re.fullmatch(PRODUCT_ID_PATTERN, value) is None:
            raise ValueError(f"{self.name[1:]} isn't in a correct form!")
        instance.__dict__[self.name] = value   

class NonNegativeInteger:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> NonNegativeInteger:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> int:
        ...

    def __get__(self, instance: object | None, owner:type) -> int | NonNegativeInteger:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{self.name[1:]} must be an integer!")
        if value < 0:
            raise ValueError(f"{self.name[1:]} must be greater or equal to zero!")
        instance.__dict__[self.name] = value

class PositiveInteger:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> PositiveInteger:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> int:
        ...

    def __get__(self, instance: object | None, owner:type) -> int | PositiveInteger:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{self.name[1:]} must be an integer!")
        if value <= 0:
            raise ValueError(f"{self.name[1:]} must be greater than zero!")
        instance.__dict__[self.name] = value

class OrderID:
    def __set_name__(self, owner:type, name:str) -> None:
        self.name = "_" + name

    @overload
    def __get__(self, instance:None, owner:type) -> OrderID:
        ...

    @overload
    def __get__(self, instance:object, owner:type) -> str:
        ...

    def __get__(self, instance: object | None, owner:type) -> str | OrderID:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance:object, value:str) -> None:
        if self.name in instance.__dict__:
            raise AttributeError(f"{self.name[1:]} cannot be modified after initialization!")
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string!")
        value = value.strip().upper()
        if re.fullmatch(ORDER_ID_PATTERN, value) is None:
            raise ValueError(f"{self.name[1:]} isn't in a correct form!")
        instance.__dict__[self.name] = value   
