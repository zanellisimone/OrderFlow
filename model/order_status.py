from enum import Enum

class OrderStatus(Enum):
    DRAFT = 1
    CONFIRMED = 2
    SHIPPED = 3
    CANCELLED = 4