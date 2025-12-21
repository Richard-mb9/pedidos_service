from uuid import UUID
from typing import Optional
from abc import ABC, abstractmethod
from domain.entities import Order
from domain.enums import OrderStatus


class OrderRepositoryInterface(ABC):

    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        raise NotImplementedError("Should implement method: find_by_id")

    @abstractmethod
    def save(self, order: Order) -> bool:
        raise NotImplementedError("Should implement method: save")

    @abstractmethod
    def update_status(self, order_id: UUID, new_status: OrderStatus) -> bool:
        raise NotImplementedError("Should implement method: update_status")
