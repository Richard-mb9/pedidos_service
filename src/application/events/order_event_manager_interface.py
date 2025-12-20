from typing import List, Optional, Dict
from abc import ABC, abstractmethod
from domain.enums import OrderStatus
from domain.entities import Order


class OrderEventManagerInterface(ABC):

    _valid_transitions: Dict[OrderStatus, List[OrderStatus]] = {
        OrderStatus.CREATED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
        OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    @abstractmethod
    def order_created_event(self, order: Order) -> "OrderEventManagerInterface":
        raise NotImplementedError("Should implement method: order_created_event")

    @abstractmethod
    def order_status_changed_event(
        self,
        order: Order,
        new_status: OrderStatus,
        older_status: OrderStatus,
        changed_by: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> "OrderEventManagerInterface":
        raise NotImplementedError("Should implement method: order_status_changed_event")

    @abstractmethod
    def order_cancelled_event(
        self,
        order: Order,
        older_status: OrderStatus,
        reason: str,
        cancelled_by: Optional[str] = None,
    ) -> "OrderEventManagerInterface":
        raise NotImplementedError("Should implement method: order_cancelled_event")

    @abstractmethod
    def clear_events(self) -> "OrderEventManagerInterface":
        raise NotImplementedError("Should implement method: clear_events")

    @abstractmethod
    def publish_events(self) -> None:
        raise NotImplementedError("Should implement method: clear_events")
