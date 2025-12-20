from uuid import UUID
from domain.enums import ErrorCategory
from .domain_exception import DomainException


class OrderAlreadyCancelledError(DomainException):
    category: ErrorCategory = ErrorCategory.FORBIDDEN

    def __init__(self, order_id: UUID):
        self.order_id = order_id
        super().__init__(f"Order {str(order_id)} is already cancelled")
