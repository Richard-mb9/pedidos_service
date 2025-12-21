from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    productId: UUID
    productName: str
    quantity: int
    unityPrice: Decimal
