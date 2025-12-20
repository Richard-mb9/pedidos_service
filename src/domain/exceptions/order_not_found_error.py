from uuid import UUID
from domain.enums import ErrorCategory
from .domain_exception import DomainException


class OrderNotFoundError(DomainException):
    category: ErrorCategory = ErrorCategory.NOT_FOUND

    def __init__(self, order_id: UUID):
        self.order_id = order_id
        super().__init__(f"Order {str(order_id)} not found")
