from typing import Optional, Any
from domain.enums import ErrorCategory


class DomainException(Exception):
    category: ErrorCategory = ErrorCategory.INTERNAL

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        self.message = message
        self.details = details if details is not None else {}
        super().__init__(message)
