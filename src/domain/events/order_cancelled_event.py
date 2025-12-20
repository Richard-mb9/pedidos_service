from uuid import UUID
from typing import Any, Optional
from decimal import Decimal

from .domain_event import DomainEvent


class OrderCancelledEvent(DomainEvent):

    event_name = "order.cancelled"

    def __init__(
        self,
        order_id: UUID,
        customer_id: UUID,
        refund_amount: Optional[Decimal] = Decimal("0"),
        cancellation_reason: Optional[str] = None,
    ):
        super().__init__()
        self.order_id = order_id
        self.customer_id = customer_id
        self.cancellation_reason = cancellation_reason
        self.refund_amount = refund_amount

    def _payload(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "cancellation_reason": self.cancellation_reason,
            "refund_amount": str(self.refund_amount),
        }
