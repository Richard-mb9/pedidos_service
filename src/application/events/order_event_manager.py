from typing import List, Optional, Dict
from application.adapters import PublisherAdapterInterface
from domain.entities import Order
from domain.enums.order_status import OrderStatus
from domain.events import (
    DomainEvent,
    OrderCreatedEvent,
    OrderCancelledEvent,
    OrderDeliveredEvent,
    OrderStatusChangedEvent,
)


class OrderEventManager:
    _valid_transitions: Dict[OrderStatus, List[OrderStatus]] = {
        OrderStatus.CREATED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
        OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    def __init__(self, publisher: PublisherAdapterInterface):
        self.__pending_events: List[DomainEvent] = []
        self.publisher = publisher

    def order_created_event(self, order: Order) -> "OrderEventManager":
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
    ) -> "OrderEventManager":
        order.validate_transition_to(new_status=new_status)

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
        elif new_status == OrderStatus.CANCELLED:
            self.__pending_events.append(
                OrderCancelledEvent(
                    order_id=order.id,
                    customer_id=order.customer_id,
                    cancellation_reason=reason,
                    refund_amount=order.total_amount,
                )
            )
        return self

    def clear_events(self) -> "OrderEventManager":
        self.__pending_events.clear()
        return self

    def publish_events(self):
        for event in self.__pending_events:
            self.publisher.publish(event_name=event.event_name, payload=event.to_dict())

        self.clear_events()
