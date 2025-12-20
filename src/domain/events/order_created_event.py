from uuid import UUID
from typing import Any
from decimal import Decimal

from .domain_event import DomainEvent


class OrderCreatedEvent(DomainEvent):

    event_name = "order.created"

    def __init__(
        self, order_id: UUID, customer_id: UUID, items_count: int, total_amount: Decimal
    ):
        super().__init__()
        self.order_id = order_id
        self.customer_id = customer_id
        self.items_count = items_count
        self.total_amount = total_amount

    def _payload(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items_count": self.items_count,
            "total_amount": str(self.total_amount),
            "initial_status": "created",
        }
