from uuid import uuid4, UUID
from decimal import Decimal
from datetime import datetime, timezone
import pytest

from domain.entities import Order, OrderItem
from domain.enums import OrderStatus
from domain.exceptions import (
    OrderAlreadyCancelledError,
    OrderAlreadyDeliveredError,
    InvalidStatusTransitionError,
)
from domain.events import (
    OrderCreatedEvent,
    OrderStatusChangedEvent,
    OrderDeliveredEvent,
    OrderCancelledEvent,
)


def test_should_create_order_with_default_values():
    customer_id = uuid4()
    shipping_address = "Test Address"
    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Decimal("100.50"),
        )
    ]

    order = Order(
        customer_id=customer_id,
        shipping_address=shipping_address,
        items=items,
    )

    assert isinstance(order.id, UUID)
    assert order.customer_id == customer_id
    assert order.shipping_address == shipping_address
    assert order.items == items
    assert order.status == OrderStatus.CREATED
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)


def test_should_create_order_with_custom_id():
    custom_id = uuid4()
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        id=custom_id,
    )

    assert order.id == custom_id


def test_should_create_order_with_custom_status():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    assert order.status == OrderStatus.PROCESSING


def test_should_create_order_with_custom_dates():
    custom_date = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        created_at=custom_date,
        updated_at=custom_date,
    )

    assert order.created_at == custom_date
    assert order.updated_at == custom_date


def test_should_calculate_total_amount():
    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Product 1",
            quantity=2,
            unit_price=Decimal("100.50"),
        ),
        OrderItem(
            product_id=uuid4(),
            product_name="Product 2",
            quantity=3,
            unit_price=Decimal("50.00"),
        ),
    ]

    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=items,
    )

    assert order.total_amount == Decimal("351.00")


def test_should_calculate_total_amount_with_single_item():
    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Product 1",
            quantity=1,
            unit_price=Decimal("99.99"),
        )
    ]

    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=items,
    )

    assert order.total_amount == Decimal("99.99")


def test_should_calculate_total_amount_with_empty_items():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    assert order.total_amount == Decimal("0")


def test_should_create_order_with_factory_method():
    customer_id = uuid4()
    shipping_address = "Test Address"
    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Decimal("100.50"),
        )
    ]

    order = Order.create(
        customer_id=customer_id,
        shipping_address=shipping_address,
        items=items,
    )

    assert isinstance(order.id, UUID)
    assert order.customer_id == customer_id
    assert order.shipping_address == shipping_address
    assert order.items == items
    assert order.status == OrderStatus.CREATED


def test_should_add_created_event_when_using_factory():
    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Decimal("100.50"),
        )
    ]

    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=items,
    )

    assert len(order.pending_events) == 1
    event = order.pending_events[0]
    assert isinstance(event, OrderCreatedEvent)
    assert event.order_id == order.id
    assert event.customer_id == order.customer_id
    assert event.items_count == len(items)
    assert event.total_amount == order.total_amount


def test_should_change_status_from_created_to_processing():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )
    order.clear_events()

    order.change_status(OrderStatus.PROCESSING)

    assert order.status == OrderStatus.PROCESSING
    assert len(order.pending_events) == 1
    event = order.pending_events[0]
    assert isinstance(event, OrderStatusChangedEvent)
    assert event.order_id == order.id
    assert event.previous_status == OrderStatus.CREATED
    assert event.new_status == OrderStatus.PROCESSING


def test_should_change_status_from_created_to_cancelled():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItem(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("100.00"),
            )
        ],
    )
    order.clear_events()

    order.change_status(OrderStatus.CANCELLED, reason="Customer request")

    assert order.status == OrderStatus.CANCELLED
    assert len(order.pending_events) == 2
    status_event = order.pending_events[0]
    cancelled_event = order.pending_events[1]
    assert isinstance(status_event, OrderStatusChangedEvent)
    assert isinstance(cancelled_event, OrderCancelledEvent)
    assert cancelled_event.cancellation_reason == "Customer request"
    assert cancelled_event.refund_amount == order.total_amount


def test_should_change_status_from_processing_to_shipped():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    order.change_status(OrderStatus.SHIPPED)

    assert order.status == OrderStatus.SHIPPED


def test_should_change_status_from_processing_to_cancelled():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    order.change_status(OrderStatus.CANCELLED)

    assert order.status == OrderStatus.CANCELLED


def test_should_change_status_from_shipped_to_delivered():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.SHIPPED,
    )

    order.change_status(OrderStatus.DELIVERED)

    assert order.status == OrderStatus.DELIVERED
    delivered_event = None
    for event in order.pending_events:
        if isinstance(event, OrderDeliveredEvent):
            delivered_event = event
            break

    assert delivered_event is not None
    assert delivered_event.order_id == order.id
    assert delivered_event.customer_id == order.customer_id
    assert delivered_event.delivery_address == order.shipping_address


def test_should_fail_to_change_cancelled_order_status():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CANCELLED,
    )

    with pytest.raises(OrderAlreadyCancelledError) as exc_info:
        order.change_status(OrderStatus.PROCESSING)

    assert exc_info.value.order_id == order.id


def test_should_fail_to_change_delivered_order_status():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.DELIVERED,
    )

    with pytest.raises(OrderAlreadyDeliveredError) as exc_info:
        order.change_status(OrderStatus.CANCELLED)

    assert exc_info.value.order_id == order.id


def test_should_fail_invalid_transition_from_created_to_shipped():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    with pytest.raises(InvalidStatusTransitionError) as exc_info:
        order.change_status(OrderStatus.SHIPPED)

    assert exc_info.value.order_id == order.id
    assert exc_info.value.current_status == OrderStatus.CREATED
    assert exc_info.value.attempted_status == OrderStatus.SHIPPED


def test_should_fail_invalid_transition_from_created_to_delivered():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    with pytest.raises(InvalidStatusTransitionError) as exc_info:
        order.change_status(OrderStatus.DELIVERED)

    assert exc_info.value.order_id == order.id
    assert exc_info.value.current_status == OrderStatus.CREATED
    assert exc_info.value.attempted_status == OrderStatus.DELIVERED


def test_should_fail_invalid_transition_from_processing_to_delivered():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    with pytest.raises(InvalidStatusTransitionError) as exc_info:
        order.change_status(OrderStatus.DELIVERED)

    assert exc_info.value.current_status == OrderStatus.PROCESSING
    assert exc_info.value.attempted_status == OrderStatus.DELIVERED


def test_should_fail_invalid_transition_from_shipped_to_processing():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.SHIPPED,
    )

    with pytest.raises(InvalidStatusTransitionError):
        order.change_status(OrderStatus.PROCESSING)


def test_should_fail_invalid_transition_from_shipped_to_cancelled():
    order = Order(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.SHIPPED,
    )

    with pytest.raises(InvalidStatusTransitionError):
        order.change_status(OrderStatus.CANCELLED)


def test_should_clear_pending_events():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    assert len(order.pending_events) > 0

    order.clear_events()

    assert len(order.pending_events) == 0


def test_should_convert_order_to_dict():
    order_id = uuid4()
    customer_id = uuid4()
    created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    updated_at = datetime(2023, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Decimal("100.50"),
        )
    ]

    order = Order(
        id=order_id,
        customer_id=customer_id,
        shipping_address="Test Address",
        items=items,
        status=OrderStatus.PROCESSING,
        created_at=created_at,
        updated_at=updated_at,
    )

    result = order.to_dict()

    assert result["id"] == str(order_id)
    assert result["customerId"] == str(customer_id)
    assert result["shippingAddress"] == "Test Address"
    assert result["status"] == "PROCESSING"
    assert result["createdAt"] == created_at.isoformat()
    assert result["updatedAt"] == updated_at.isoformat()
    assert len(result["items"]) == 1


def test_should_convert_order_to_dict_with_correct_types():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    result = order.to_dict()

    assert isinstance(result["id"], str)
    assert isinstance(result["customerId"], str)
    assert isinstance(result["shippingAddress"], str)
    assert isinstance(result["status"], str)
    assert isinstance(result["createdAt"], str)
    assert isinstance(result["updatedAt"], str)
    assert isinstance(result["items"], list)


def test_should_validate_transition_successfully():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    order.validate_transition_to(OrderStatus.PROCESSING)


def test_should_add_status_changed_event_with_metadata():
    order = Order.create(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )
    order.clear_events()

    order.change_status(
        OrderStatus.PROCESSING,
        changed_by="admin@example.com",
        reason="Manual processing",
    )

    event = order.pending_events[0]
    assert isinstance(event, OrderStatusChangedEvent)
    assert event.changed_by == "admin@example.com"
    assert event.reason == "Manual processing"
