from application.repositories import OrderRepositoryInterface
from application.dtos import CreateOrderDTO
from application.events import OrderEventManager

from domain.entities import Order, OrderItem


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        order_event_manager: OrderEventManager,
    ):
        self.repository = repository
        self.order_event_manager = order_event_manager

    def execute(self, data: CreateOrderDTO) -> Order:
        order = Order(
            customer_id=data.customer_id,
            shipping_address=data.shipping_address,
            items=[
                OrderItem(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in data.items
            ],
        )

        self.order_event_manager.order_created_event(order=order).publish_events()

        return order
