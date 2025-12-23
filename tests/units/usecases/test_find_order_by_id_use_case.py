from uuid import uuid4
from decimal import Decimal
import pytest
from mockito import mock, when, verify

from application.use_cases import FindOrderByIdUseCase
from application.repositories import OrderRepositoryInterface
from domain.entities import Order, OrderItem
from domain.exceptions import OrderNotFoundError
from domain.enums import OrderStatus


def test_should_find_order_by_id():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    result = use_case.execute(order_id)

    assert result is not None
    assert result == expected_order
    assert result.id == order_id


def test_should_call_repository_find_by_id():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    use_case.execute(order_id)

    verify(repository, times=1).find_by_id(order_id=order_id)


def test_should_return_none_when_order_not_found():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()

    when(repository).find_by_id(order_id=order_id).thenReturn(None)

    result = use_case.execute(order_id)

    assert result is None


def test_should_raise_exception_when_order_not_found_and_raise_flag_is_true():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()

    when(repository).find_by_id(order_id=order_id).thenReturn(None)

    with pytest.raises(OrderNotFoundError) as exc_info:
        use_case.execute(order_id, raise_if_is_none=True)

    assert exc_info.value.order_id == order_id


def test_should_not_raise_exception_when_order_not_found_and_raise_flag_is_false():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()

    when(repository).find_by_id(order_id=order_id).thenReturn(None)

    result = use_case.execute(order_id, raise_if_is_none=False)

    assert result is None


def test_should_find_order_with_items():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    items = [
        OrderItem(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Decimal("100.50"),
        )
    ]
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=items,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    result = use_case.execute(order_id)

    assert result is not None
    assert len(result.items) == 1
    assert result.items[0].product_name == "Test Product"


def test_should_find_order_with_different_statuses():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.PROCESSING,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    result = use_case.execute(order_id)
    assert result is not None
    assert result.status == OrderStatus.PROCESSING


def test_should_find_cancelled_order():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.CANCELLED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    result = use_case.execute(order_id)
    assert result is not None
    assert result.status == OrderStatus.CANCELLED


def test_should_find_delivered_order():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
        status=OrderStatus.DELIVERED,
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    result = use_case.execute(order_id)

    assert result is not None
    assert result.status == OrderStatus.DELIVERED


def test_should_return_order_when_found_and_raise_flag_is_true():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id = uuid4()
    expected_order = Order(
        id=order_id,
        customer_id=uuid4(),
        shipping_address="Test Address",
        items=[],
    )

    when(repository).find_by_id(order_id=order_id).thenReturn(expected_order)

    result = use_case.execute(order_id, raise_if_is_none=True)

    assert result == expected_order


def test_should_handle_multiple_different_order_ids():
    repository = mock(OrderRepositoryInterface)
    use_case = FindOrderByIdUseCase(repository)

    order_id_1 = uuid4()
    order_id_2 = uuid4()

    order_1 = Order(
        id=order_id_1,
        customer_id=uuid4(),
        shipping_address="Address 1",
        items=[],
    )
    order_2 = Order(
        id=order_id_2,
        customer_id=uuid4(),
        shipping_address="Address 2",
        items=[],
    )

    when(repository).find_by_id(order_id=order_id_1).thenReturn(order_1)
    when(repository).find_by_id(order_id=order_id_2).thenReturn(order_2)

    result_1 = use_case.execute(order_id_1)
    result_2 = use_case.execute(order_id_2)

    assert result_1 is not None
    assert result_2 is not None
    assert result_1.id == order_id_1
    assert result_2.id == order_id_2
    assert result_1.shipping_address == "Address 1"
    assert result_2.shipping_address == "Address 2"
