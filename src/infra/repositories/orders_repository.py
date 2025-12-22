from typing import Dict, Any, Optional, cast
from datetime import datetime
from uuid import UUID
from application.repositories import OrderRepositoryInterface
from domain.entities import Order, OrderItem
from domain.enums.order_status import OrderStatus

from infra.adapters import NoSqlAdapter


class OrdersRepository(OrderRepositoryInterface):
    def __init__(self, adapter: NoSqlAdapter) -> None:
        self.adapter = adapter
        self.collection = adapter.database["orders"]

    def from_dict(self, document: Dict[str, Any]) -> Order:
        return Order(
            id=UUID(document.get("id")),
            customer_id=UUID(document.get("customerId")),
            shipping_address=document.get("shippingAddress", ""),
            status=OrderStatus[document.get("status", "")],
            created_at=datetime.fromisoformat(document.get("createdAt", "")),
            updated_at=datetime.fromisoformat(document.get("createdAt", "")),
            items=[
                OrderItem(
                    product_id=UUID(item.get("productId")),
                    product_name=item.get("productName"),
                    quantity=item.get("quantity"),
                    unit_price=item.get("unitPrice"),
                )
                for item in document.get("items", [])
            ],
        )

    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        order_document = cast(
            Optional[Dict[str, Any]],
            self.collection.find_one({"id": str(order_id)}),
        )
        if order_document is not None:
            return self.from_dict(order_document)

    def save(self, order: Order) -> bool:
        self.collection.insert_one(order.to_dict())
        return True

    def update_status(self, order_id: UUID, new_status: OrderStatus) -> bool:
        filter = {"id": str(order_id)}
        new_data = {
            "$set": {
                "status": new_status.value,
                "updatedAt": datetime.now().isoformat(),
            }
        }
        self.collection.update_one(filter=filter, update=new_data)
        return True
