from uuid import UUID
from typing import Any
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItem:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

    def to_dict(self) -> dict[str, Any]:
        return {
            "productId": str(self.product_id),
            "productName": self.product_name,
            "quantity": self.quantity,
            "unitPrice": self.unit_price,
            "subtotal": self.subtotal,
        }
