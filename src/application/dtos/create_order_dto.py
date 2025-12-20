from uuid import UUID
from typing import Optional, List
from dataclasses import dataclass, field
from .order_item_dto import OrderItemDTO


@dataclass(frozen=True)
class CreateOrderDTO:
    customer_id: UUID
    shipping_address: str
    items: List[OrderItemDTO]
    id: Optional[UUID] = field(default_factory=lambda: None)
