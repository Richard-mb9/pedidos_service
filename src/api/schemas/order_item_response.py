from uuid import UUID
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrderItemResponse:
    productId: UUID
    productName: str
    quantity: int
    unityPrice: Decimal
