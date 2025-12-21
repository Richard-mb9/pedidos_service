from uuid import UUID
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrderResponse:
    orderId: UUID
