from uuid import UUID
from application.repositories import OrderRepositoryInterface
from application.adapters import PublisherAdapterInterface
from domain.enums import OrderStatus
from .find_order_by_id_use_case import FindOrderByIdUseCase


class UpdateOrderStatusUseCase:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        publisher: PublisherAdapterInterface,
    ):
        self.repository = repository
        self.publisher = publisher
        self.__find_order_by_id = FindOrderByIdUseCase(repository).execute

    def execute(self, order_id: UUID, new_status: OrderStatus):
        order = self.__find_order_by_id(order_id=order_id, raise_if_is_none=True)  # type: ignore
        if order:
            order.change_status(new_status=new_status)
            self.repository.update_status(
                order_id=order_id,
                new_status=new_status,
            )

            self.publisher.publish_events(order.pending_events)
