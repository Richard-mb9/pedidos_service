from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrderItemDTO:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal
