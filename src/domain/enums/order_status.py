from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
