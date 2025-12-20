from uuid import UUID
from typing import Any
from datetime import datetime, timezone

from .domain_event import DomainEvent


class OrderDeliveredEvent(DomainEvent):

    event_name = "oder.delivered"

    def __init__(
        self,
        order_id: UUID,
        customer_id: UUID,
        delivery_address: str,
        delivered_at: datetime = datetime.now(timezone.utc),
    ):
        super().__init__()
        self.order_id = order_id
        self.customer_id = customer_id
        self.delivery_address = delivery_address
        self.delivered_at = delivered_at

    def _payload(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "delivery_address": self.delivery_address,
            "delivered_at": self.delivered_at.isoformat(),
        }
