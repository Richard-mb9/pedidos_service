from typing import List, Optional
from uuid import UUID
from application.repositories import OrderRepositoryInterface
from domain.entities import Order
from domain.enums.order_status import OrderStatus


class FakeOrderRepository(OrderRepositoryInterface):

    def __init__(self):
        self.data: List[Order] = []

    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        for item in self.data:
            if str(item.id) == str(order_id):
                return item

    def save(self, order: Order) -> bool:
        self.data.append(order)
        return True

    def update_status(self, order_id: UUID, new_status: OrderStatus) -> bool:
        for order in self.data:
            if order.id == order_id:
                order.status = new_status
                return True

        return False

    def clear_data(self):
        self.data = []


fake_order_repository = FakeOrderRepository()
