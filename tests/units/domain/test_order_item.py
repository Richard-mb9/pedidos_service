from uuid import uuid4
from decimal import Decimal

from domain.entities import OrderItem


def test_should_create_order_item():
    product_id = uuid4()
    product_name = "Test Product"
    quantity = 2
    unit_price = Decimal("100.50")

    order_item = OrderItem(
        product_id=product_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
    )

    assert order_item.product_id == product_id
    assert order_item.product_name == product_name
    assert order_item.quantity == quantity
    assert order_item.unit_price == unit_price


def test_should_calculate_subtotal_correctly():
    order_item = OrderItem(
        product_id=uuid4(),
        product_name="Test Product",
        quantity=3,
        unit_price=Decimal("50.00"),
    )

    assert order_item.subtotal == Decimal("150.00")


def test_should_calculate_subtotal_with_decimal_values():
    order_item = OrderItem(
        product_id=uuid4(),
        product_name="Test Product",
        quantity=2,
        unit_price=Decimal("99.99"),
    )

    assert order_item.subtotal == Decimal("199.98")


def test_should_calculate_subtotal_with_single_quantity():
    order_item = OrderItem(
        product_id=uuid4(),
        product_name="Test Product",
        quantity=1,
        unit_price=Decimal("75.50"),
    )

    assert order_item.subtotal == Decimal("75.50")


def test_should_convert_to_dict():
    product_id = uuid4()
    order_item = OrderItem(
        product_id=product_id,
        product_name="Test Product",
        quantity=2,
        unit_price=Decimal("100.50"),
    )

    result = order_item.to_dict()

    assert result["productId"] == str(product_id)
    assert result["productName"] == "Test Product"
    assert result["quantity"] == 2
    assert result["unitPrice"] == 100.50
    assert result["subtotal"] == 201.00


def test_should_convert_to_dict_with_correct_types():
    order_item = OrderItem(
        product_id=uuid4(),
        product_name="Test Product",
        quantity=3,
        unit_price=Decimal("25.99"),
    )

    result = order_item.to_dict()

    assert isinstance(result["productId"], str)
    assert isinstance(result["productName"], str)
    assert isinstance(result["quantity"], int)
    assert isinstance(result["unitPrice"], float)
    assert isinstance(result["subtotal"], float)
