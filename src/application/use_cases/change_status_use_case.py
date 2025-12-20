from uuid import UUID
from datetime import datetime, timezone
from application.repositories import OrderRepositoryInterface
from application.events import OrderEventManager
from domain.enums import OrderStatus
from .find_order_by_id_use_case import FindOrderByIdUseCase


class ChangeStatusUseCase:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        order_event_manager: OrderEventManager,
    ):
        self.repository = repository
        self.order_event_manager = order_event_manager
        self.__find_order_by_id = FindOrderByIdUseCase(repository).execute

    def execute(self, order_id: UUID, new_status: OrderStatus):
        order = self.__find_order_by_id(order_id=order_id, raise_if_is_none=True)  # type: ignore
        if order:
            order.validate_transition_to(new_status)
            self.repository.update_status(
                order_id=order_id,
                new_status=new_status,
                updated_at=datetime.now(timezone.utc),
            )

            self.order_event_manager.order_status_changed_event(
                order=order,
                new_status=new_status,
                older_status=order.status,
            )
