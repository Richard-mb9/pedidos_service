from enum import Enum


class ErrorCategory(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    VALIDATION = "VALIDATION"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL = "INTERNAL"
