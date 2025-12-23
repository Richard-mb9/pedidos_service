from uuid import uuid4
import pytest
from mockito import mock, when, verify

from application.use_cases import UpdateOrderStatusUseCase
from application.repositories import OrderRepositoryInterface
from application.adapters import PublisherAdapterInterface
from domain.enums import OrderStatus
from domain.entities import Order
from domain.events import DomainEvent
from domain.exceptions import (
    OrderNotFoundError,
    InvalidStatusTransitionError,
    OrderAlreadyCancelledError,
    OrderAlreadyDeliveredError,
)


def test_should_update_order_status_from_created_to_processing():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.PROCESSING
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.PROCESSING)

    assert order.status == OrderStatus.PROCESSING


def test_should_call_repository_update_status():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.PROCESSING
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.PROCESSING)

    verify(repository, times=1).update_status(
        order_id=order_id, new_status=OrderStatus.PROCESSING
    )


def test_should_call_publisher_publish_events():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.PROCESSING
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.PROCESSING)

    verify(publisher, times=1).publish_events(...)


def test_should_raise_exception_when_order_not_found():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()

    when(repository).find_by_id(order_id=order_id).thenReturn(None)

    with pytest.raises(OrderNotFoundError) as exc_info:
        use_case.execute(order_id, OrderStatus.PROCESSING)

    assert exc_info.value.order_id == order_id


def test_should_update_from_created_to_cancelled():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.CANCELLED
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.CANCELLED)

    assert order.status == OrderStatus.CANCELLED


def test_should_update_from_processing_to_shipped():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.SHIPPED
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.SHIPPED)

    assert order.status == OrderStatus.SHIPPED


def test_should_update_from_processing_to_cancelled():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.CANCELLED
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.CANCELLED)

    assert order.status == OrderStatus.CANCELLED


def test_should_update_from_shipped_to_delivered():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.SHIPPED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.DELIVERED
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.DELIVERED)

    assert order.status == OrderStatus.DELIVERED


def test_should_fail_invalid_transition_from_created_to_shipped():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)

    with pytest.raises(InvalidStatusTransitionError):
        use_case.execute(order_id, OrderStatus.SHIPPED)


def test_should_fail_invalid_transition_from_created_to_delivered():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)

    with pytest.raises(InvalidStatusTransitionError):
        use_case.execute(order_id, OrderStatus.DELIVERED)


def test_should_fail_to_update_cancelled_order():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CANCELLED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)

    with pytest.raises(OrderAlreadyCancelledError):
        use_case.execute(order_id, OrderStatus.PROCESSING)


def test_should_fail_to_update_delivered_order():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.DELIVERED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)

    with pytest.raises(OrderAlreadyDeliveredError):
        use_case.execute(order_id, OrderStatus.CANCELLED)


def test_should_publish_status_changed_event():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    published_events = None

    def capture_events(events: DomainEvent):
        nonlocal published_events
        published_events = events

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.PROCESSING
    ).thenReturn(True)
    when(publisher).publish_events(...).thenAnswer(capture_events)

    use_case.execute(order_id, OrderStatus.PROCESSING)

    assert published_events is not None
    assert len(published_events) > 0


def test_should_publish_delivered_event_when_status_is_delivered():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.SHIPPED,
    )

    published_events = None

    def capture_events(events: DomainEvent):
        nonlocal published_events
        published_events = events

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.DELIVERED
    ).thenReturn(True)
    when(publisher).publish_events(...).thenAnswer(capture_events)

    use_case.execute(order_id, OrderStatus.DELIVERED)

    assert published_events is not None
    assert len(published_events) == 2


def test_should_publish_cancelled_event_when_status_is_cancelled():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    published_events = None

    def capture_events(events: DomainEvent):
        nonlocal published_events
        published_events = events

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.CANCELLED
    ).thenReturn(True)
    when(publisher).publish_events(...).thenAnswer(capture_events)

    use_case.execute(order_id, OrderStatus.CANCELLED)

    assert published_events is not None
    assert len(published_events) == 2


def test_should_call_find_by_id_before_update():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()
    order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CREATED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(order)
    when(repository).update_status(
        order_id=order_id, new_status=OrderStatus.PROCESSING
    ).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(order_id, OrderStatus.PROCESSING)

    verify(repository, times=1).find_by_id(order_id=order_id)


def test_should_not_update_when_order_is_none():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = UpdateOrderStatusUseCase(repository, publisher)

    order_id = uuid4()

    when(repository).find_by_id(order_id=order_id).thenReturn(None)

    with pytest.raises(OrderNotFoundError):
        use_case.execute(order_id, OrderStatus.PROCESSING)

    verify(repository, times=0).update_status(...)
    verify(publisher, times=0).publish_events(...)
