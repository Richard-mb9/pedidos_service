from typing import List, Any
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4, UUID

from domain.enums.order_status import OrderStatus

from .order_item import OrderItem


class Order:
    def __init__(
        self,
        customer_id: UUID,
        shipping_address: str,
        items: List[OrderItem],
        id: UUID = uuid4(),
        status: OrderStatus = OrderStatus.CREATED,
    ):
        self.id = id
        self.customer_id = customer_id
        self.shipping_address = shipping_address
        self.items = items
        self.status = status
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        self._pending_events = []

    @property
    def total_amount(self) -> Decimal:
        total = Decimal("0")
        for item in self.items:
            total += item.subtotal
        return total

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "customerId": str(self.customer_id),
            "shippingAddress": self.shipping_address,
            "status": self.status.value,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "items": [item.to_dict() for item in self.items],
        }
