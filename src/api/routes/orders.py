from uuid import UUID
from http import HTTPStatus

from fastapi import APIRouter

from api.schemas import (
    OrderResponse,
    CreateOrderResponse,
    CreateOrderRequest,
    UpdateOrderStatusRequest,
)
from api.controllers import OrdersController

router = APIRouter()


@router.get("/{orderId}", status_code=HTTPStatus.OK, response_model=OrderResponse)
async def list_order_by_id(orderId: UUID):
    return OrdersController().find_order_by_id(orderId)


@router.post("", status_code=HTTPStatus.CREATED, response_model=CreateOrderResponse)
async def create_order(data: CreateOrderRequest):
    return OrdersController().create(data=data)


@router.patch("/{orderId}", status_code=HTTPStatus.NO_CONTENT)
async def update_order_status(orderId: UUID, data: UpdateOrderStatusRequest):
    OrdersController().update_order_status(order_id=orderId, data=data)
