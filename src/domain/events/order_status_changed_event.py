from uuid import UUID
from typing import Any, Optional

from domain.enums import OrderStatus
from .domain_event import DomainEvent


class OrderStatusChangedEvent(DomainEvent):
    event_name = "order.changedStatus"

    def __init__(
        self,
        order_id: UUID,
        previous_status: OrderStatus,
        new_status: OrderStatus,
        changed_by: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        super().__init__()
        self.order_id = order_id
        self.previous_status = previous_status
        self.new_status = new_status
        self.changed_by = changed_by
        self.reason = reason

    def _payload(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "previous_status": self.previous_status.value,
            "new_status": self.new_status.value,
            "changed_by": self.changed_by,
            "reason": self.reason,
        }
