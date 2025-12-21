from pydantic import BaseModel

from domain.enums import OrderStatus


class UpdateOrderStatusRequest(BaseModel):
    newStatus: OrderStatus
