from application.repositories import OrderRepositoryInterface
from application.dtos import CreateOrderDTO
from application.adapters import PublisherAdapterInterface

from domain.entities import Order, OrderItem


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        publisher: PublisherAdapterInterface,
    ):
        self.repository = repository
        self.publisher = publisher

    def execute(self, data: CreateOrderDTO) -> Order:
        order = Order.create(
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
        self.repository.save(order)
        self.publisher.publish_events(order.pending_events)

        return order
