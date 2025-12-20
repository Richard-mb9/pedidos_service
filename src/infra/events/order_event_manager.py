from typing import List, Optional
from application.events import OrderEventManagerInterface
from application.adapters import PublisherAdapterInterface
from domain.entities import Order
from domain.enums.order_status import OrderStatus
from domain.exceptions import OrderAlreadyCancelledError, InvalidStatusTransitionError
from domain.events import (
    DomainEvent,
    OrderCreatedEvent,
    OrderCancelledEvent,
    OrderDeliveredEvent,
    OrderStatusChangedEvent,
)


class OrderEventManager(OrderEventManagerInterface):
    def __init__(self, publisher: PublisherAdapterInterface):
        self.__pending_events: List[DomainEvent] = []
        self.publisher = publisher

    def order_created_event(self, order: Order) -> OrderEventManagerInterface:
        self.__pending_events.append(
            OrderCreatedEvent(
                order_id=order.id,
                customer_id=order.customer_id,
                items_count=len(order.items),
                total_amount=order.total_amount,
            )
        )

        return self

    def order_status_changed_event(
        self,
        order: Order,
        new_status: OrderStatus,
        older_status: OrderStatus,
        changed_by: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> OrderEventManagerInterface:
        self.__validate_transition_to(
            order=order, current_status=older_status, new_status=new_status
        )

        self.__pending_events.append(
            OrderStatusChangedEvent(
                order_id=order.id,
                previous_status=older_status,
                new_status=new_status,
                changed_by=changed_by,
                reason=reason,
            )
        )

        if new_status == OrderStatus.DELIVERED:
            self.__pending_events.append(
                OrderDeliveredEvent(
                    order_id=order.id,
                    customer_id=order.customer_id,
                    delivery_address=order.shipping_address,
                )
            )

        return self

    def order_cancelled_event(
        self,
        order: Order,
        older_status: OrderStatus,
        reason: str,
        cancelled_by: Optional[str] = None,
    ) -> OrderEventManagerInterface:
        self.__validate_transition_to(
            order=order, current_status=older_status, new_status=OrderStatus.CANCELLED
        )

        self.__pending_events.append(
            OrderStatusChangedEvent(
                order_id=order.id,
                previous_status=older_status,
                new_status=OrderStatus.CANCELLED,
                changed_by=cancelled_by,
                reason=reason,
            )
        )

        self.__pending_events.append(
            OrderCancelledEvent(
                order_id=order.id,
                customer_id=order.customer_id,
                cancellation_reason=reason,
                refund_amount=order.total_amount,
            )
        )

        return self

    def clear_events(self) -> OrderEventManagerInterface:
        self.__pending_events.clear()
        return self

    def publish_events(self):
        for event in self.__pending_events:
            self.publisher.publish(event_name=event.event_name, payload=event.to_dict())

        self.clear_events()

    def __validate_transition_to(
        self, order: Order, current_status: OrderStatus, new_status: OrderStatus
    ) -> None:
        if new_status not in self._valid_transitions.get(current_status, []):
            raise InvalidStatusTransitionError(
                order_id=order.id,
                current_status=current_status,
                attempted_status=new_status,
            )

        if current_status == OrderStatus.CANCELLED:
            raise OrderAlreadyCancelledError(order_id=order.id)
