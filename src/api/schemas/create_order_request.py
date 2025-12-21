from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel

from .order_item_request import OrderItemRequest


class CreateOrderRequest(BaseModel):
    customerId: UUID
    shippingAddress: str
    items: List[OrderItemRequest]
    id: Optional[UUID] = None
