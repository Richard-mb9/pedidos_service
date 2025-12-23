from uuid import uuid4
from decimal import Decimal
from mockito import mock, when, verify

from application.use_cases import CreateOrderUseCase
from application.repositories import OrderRepositoryInterface
from application.adapters import PublisherAdapterInterface
from application.dtos import CreateOrderDTO, OrderItemDTO
from domain.entities import Order
from domain.enums import OrderStatus
from domain.events import DomainEvent


def test_should_create_order_successfully():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    customer_id = uuid4()
    items = [
        OrderItemDTO(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Decimal("100.50"),
        )
    ]
    dto = CreateOrderDTO(
        customer_id=customer_id,
        shipping_address="Test Address",
        items=items,
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    result = use_case.execute(dto)

    assert isinstance(result, Order)
    assert result.customer_id == customer_id
    assert result.shipping_address == "Test Address"
    assert len(result.items) == 1
    assert result.status == OrderStatus.CREATED


def test_should_call_repository_save():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItemDTO(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("50.00"),
            )
        ],
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(dto)

    verify(repository, times=1).save(...)


def test_should_call_publisher_publish_events():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItemDTO(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("50.00"),
            )
        ],
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    use_case.execute(dto)

    verify(publisher, times=1).publish_events(...)


def test_should_create_order_with_multiple_items():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    items = [
        OrderItemDTO(
            product_id=uuid4(),
            product_name="Product 1",
            quantity=2,
            unit_price=Decimal("100.50"),
        ),
        OrderItemDTO(
            product_id=uuid4(),
            product_name="Product 2",
            quantity=3,
            unit_price=Decimal("50.00"),
        ),
    ]
    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=items,
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    result = use_case.execute(dto)

    assert len(result.items) == 2
    assert result.items[0].product_name == "Product 1"
    assert result.items[1].product_name == "Product 2"


def test_should_create_order_items_with_correct_attributes():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    product_id = uuid4()
    items = [
        OrderItemDTO(
            product_id=product_id,
            product_name="Test Product",
            quantity=5,
            unit_price=Decimal("25.99"),
        )
    ]
    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=items,
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    result = use_case.execute(dto)

    order_item = result.items[0]
    assert order_item.product_id == product_id
    assert order_item.product_name == "Test Product"
    assert order_item.quantity == 5
    assert order_item.unit_price == Decimal("25.99")


def test_should_create_order_with_pending_events():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItemDTO(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("100.00"),
            )
        ],
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    result = use_case.execute(dto)

    assert len(result.pending_events) > 0


def test_should_publish_order_created_event():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItemDTO(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("100.00"),
            )
        ],
    )

    published_events = None

    def capture_events(events: DomainEvent):
        nonlocal published_events
        published_events = events

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenAnswer(capture_events)

    use_case.execute(dto)

    assert published_events is not None
    assert len(published_events) > 0


def test_should_create_order_with_default_status():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItemDTO(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("100.00"),
            )
        ],
    )

    when(repository).save(...).thenReturn(True)
    when(publisher).publish_events(...).thenReturn(None)

    result = use_case.execute(dto)

    assert result.status == OrderStatus.CREATED


def test_should_save_order_before_publishing_events():
    repository = mock(OrderRepositoryInterface)
    publisher = mock(PublisherAdapterInterface)
    use_case = CreateOrderUseCase(repository, publisher)

    dto = CreateOrderDTO(
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[
            OrderItemDTO(
                product_id=uuid4(),
                product_name="Test Product",
                quantity=1,
                unit_price=Decimal("100.00"),
            )
        ],
    )

    call_order = []

    when(repository).save(...).thenAnswer(
        lambda order: call_order.append("save") or True  # type: ignore
    )
    when(publisher).publish_events(...).thenAnswer(
        lambda events: call_order.append("publish")  # type: ignore
    )

    use_case.execute(dto)

    assert call_order == ["save", "publish"]
