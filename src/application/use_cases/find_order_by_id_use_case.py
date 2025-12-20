from uuid import UUID
from application.repositories import OrderRepositoryInterface
from domain.exceptions import OrderNotFoundError


class FindOrderByIdUseCase:
    def __init__(self, repository: OrderRepositoryInterface):
        self.repository = repository

    def execute(self, order_id: UUID, raise_if_is_none: bool = False):
        order = self.repository.find_by_id(order_id=order_id)
        if raise_if_is_none is True and order is None:
            raise OrderNotFoundError(order_id=order_id)
        return order
