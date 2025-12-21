from uuid import UUID
from typing import cast

from domain.entities import Order

from application.use_cases import (
    CreateOrderUseCase,
    FindOrderByIdUseCase,
    UpdateOrderStatusUseCase,
)

from application.dtos import CreateOrderDTO, OrderItemDTO
from application.events import OrderEventManager

from infra.repositories import OrdersRepository
from infra.adapters import NoSqlAdapter, PublisherAdapter

from api.schemas import (
    CreateOrderRequest,
    CreateOrderResponse,
    OrderItemResponse,
    OrderResponse,
    UpdateOrderStatusRequest,
)


class OrdersController:
    def __init__(self) -> None:
        self.order_reposieoty = OrdersRepository(adapter=NoSqlAdapter())
        self.order_event_manager = OrderEventManager(PublisherAdapter())

    def create(self, data: CreateOrderRequest) -> CreateOrderResponse:
        use_case = CreateOrderUseCase(
            repository=self.order_reposieoty,
            order_event_manager=self.order_event_manager,
        )

        dto = CreateOrderDTO(
            customer_id=data.customerId,
            shipping_address=data.shippingAddress,
            items=[
                OrderItemDTO(
                    product_id=item.productId,
                    product_name=item.productName,
                    quantity=item.quantity,
                    unit_price=item.unityPrice,
                )
                for item in data.items
            ],
        )

        order = use_case.execute(data=dto)

        return CreateOrderResponse(orderId=order.id)

    def find_order_by_id(self, order_id: UUID) -> OrderResponse:
        user_case = FindOrderByIdUseCase(repository=self.order_reposieoty)

        order = cast(Order, user_case.execute(order_id=order_id, raise_if_is_none=True))
        return OrderResponse(
            id=order.id,
            customerId=order.customer_id,
            shippingAddress=order.shipping_address,
            status=order.status,
            createdAt=order.created_at,
            updatedAt=order.updated_at,
            items=[
                OrderItemResponse(
                    productId=item.product_id,
                    productName=item.product_name,
                    quantity=item.quantity,
                    unityPrice=item.unit_price,
                )
                for item in order.items
            ],
        )

    def update_order_status(
        self, order_id: UUID, data: UpdateOrderStatusRequest
    ) -> None:
        use_case = UpdateOrderStatusUseCase(
            repository=self.order_reposieoty,
            order_event_manager=self.order_event_manager,
        )

        use_case.execute(order_id=order_id, new_status=data.newStatus)
