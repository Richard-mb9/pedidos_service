from typing import List
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from domain.enums import OrderStatus
from .order_item_response import OrderItemResponse


@dataclass(frozen=True)
class OrderResponse:
    id: UUID
    customerId: UUID
    shippingAddress: str
    status: OrderStatus
    createdAt: datetime
    updatedAt: datetime
    items: List[OrderItemResponse]
