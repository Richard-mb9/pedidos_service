from typing import List, Any, Dict, Optional
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4, UUID

from domain.enums.order_status import OrderStatus
from domain.exceptions import (
    OrderAlreadyCancelledError,
    InvalidStatusTransitionError,
    OrderAlreadyDeliveredError,
)

from domain.events import (
    DomainEvent,
    OrderCreatedEvent,
    OrderStatusChangedEvent,
    OrderDeliveredEvent,
    OrderCancelledEvent,
)

from .order_item import OrderItem


class Order:
    _valid_transitions: Dict[OrderStatus, List[OrderStatus]] = {
        OrderStatus.CREATED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
        OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    def __init__(
        self,
        customer_id: UUID,
        shipping_address: str,
        items: List[OrderItem],
        id: Optional[UUID] = None,
        status: Optional[OrderStatus] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id if id is not None else uuid4()
        self.customer_id = customer_id
        self.shipping_address = shipping_address
        self.items = items
        self.status = status if status is not None else OrderStatus.CREATED
        self.created_at = (
            created_at if created_at is not None else datetime.now(timezone.utc)
        )
        self.updated_at = (
            updated_at if updated_at is not None else datetime.now(timezone.utc)
        )
        self.__pending_events: List[DomainEvent] = []

    @property
    def total_amount(self) -> Decimal:
        total = Decimal("0")
        for item in self.items:
            total += Decimal(item.subtotal)
        return total

    @property
    def pending_events(self) -> List[DomainEvent]:
        return self.__pending_events

    def __add_event(self, event: DomainEvent):
        self.__pending_events.append(event)

    def clear_events(self):
        self.__pending_events.clear()

    def validate_transition_to(self, new_status: OrderStatus):
        if self.status == OrderStatus.CANCELLED:
            raise OrderAlreadyCancelledError(order_id=self.id)
        elif self.status == OrderStatus.DELIVERED:
            raise OrderAlreadyDeliveredError(order_id=self.id)

        if new_status not in self._valid_transitions.get(self.status, []):
            raise InvalidStatusTransitionError(
                order_id=self.id,
                current_status=self.status,
                attempted_status=new_status,
            )

    @classmethod
    def create(
        cls, customer_id: UUID, shipping_address: str, items: List[OrderItem]
    ) -> "Order":

        order = cls(
            customer_id=customer_id, shipping_address=shipping_address, items=items
        )

        order.__add_event(
            OrderCreatedEvent(
                order_id=order.id,
                customer_id=order.customer_id,
                items_count=len(order.items),
                total_amount=order.total_amount,
            )
        )

        return order

    def change_status(
        self,
        new_status: OrderStatus,
        changed_by: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        self.validate_transition_to(new_status)
        self.__add_event(
            OrderStatusChangedEvent(
                self.id,
                previous_status=self.status,
                new_status=new_status,
                changed_by=changed_by,
                reason=reason,
            )
        )

        if new_status == OrderStatus.DELIVERED:
            self.__pending_events.append(
                OrderDeliveredEvent(
                    order_id=self.id,
                    customer_id=self.customer_id,
                    delivery_address=self.shipping_address,
                )
            )
        elif new_status == OrderStatus.CANCELLED:
            self.__pending_events.append(
                OrderCancelledEvent(
                    order_id=self.id,
                    customer_id=self.customer_id,
                    cancellation_reason=reason,
                    refund_amount=self.total_amount,
                )
            )

        self.status = new_status

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "customerId": str(self.customer_id),
            "shippingAddress": self.shipping_address,
            "status": self.status.value.upper(),
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "items": [item.to_dict() for item in self.items],
        }
