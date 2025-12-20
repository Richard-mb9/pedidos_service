from uuid import UUID

from domain.enums import ErrorCategory, OrderStatus
from .domain_exception import DomainException


class InvalidStatusTransitionError(DomainException):

    category: ErrorCategory = ErrorCategory.FORBIDDEN

    def __init__(
        self, order_id: UUID, current_status: OrderStatus, attempted_status: OrderStatus
    ):
        self.order_id = order_id
        self.current_status = current_status
        self.attempted_status = attempted_status
        super().__init__(
            f"Cannot transition order {str(order_id)} from '{current_status.value}' to '{attempted_status.value}'"
        )
