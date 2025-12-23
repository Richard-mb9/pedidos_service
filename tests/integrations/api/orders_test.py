from http import HTTPStatus
from uuid import UUID, uuid4
from tests.fixtures.app import Client
from tests.fixtures.repositories.fake_order_repository import fake_order_repository
from domain.enums import OrderStatus

DEFAULT_ORDER = {
    "customerId": "87d8e330-2878-4742-a86f-dbbb3bf522ac",
    "shippingAddress": "Rua Teste, 123",
    "items": [
        {
            "productId": "dcd53ddb-8104-4e48-8cc0-5df1088c6113",
            "productName": "Produto Teste",
            "quantity": 2,
            "unityPrice": 100.50,
        }
    ],
}


def test_should_create_an_order(client: Client):
    response = client.post("/orders", data=DEFAULT_ORDER)

    assert response.status_code == HTTPStatus.CREATED
    order_id = response.json().get("orderId", "")

    order_created = fake_order_repository.find_by_id(order_id)
    assert order_created is not None
    assert order_created.customer_id == UUID(DEFAULT_ORDER["customerId"])
    assert order_created.shipping_address == DEFAULT_ORDER["shippingAddress"]
    assert order_created.status == OrderStatus.CREATED
    assert len(order_created.items) == len(DEFAULT_ORDER["items"])


def test_should_create_order_with_multiple_items(client: Client):
    order_data = {
        "customerId": "87d8e330-2878-4742-a86f-dbbb3bf522ac",
        "shippingAddress": "Rua Teste, 456",
        "items": [
            {
                "productId": "dcd53ddb-8104-4e48-8cc0-5df1088c6113",
                "productName": "Produto 1",
                "quantity": 1,
                "unityPrice": 50.00,
            },
            {
                "productId": "aaa53ddb-8104-4e48-8cc0-5df1088c6114",
                "productName": "Produto 2",
                "quantity": 3,
                "unityPrice": 30.00,
            },
        ],
    }

    response = client.post("/orders", data=order_data)

    assert response.status_code == HTTPStatus.CREATED
    order_id = response.json().get("orderId", "")
    order_created = fake_order_repository.find_by_id(order_id)
    assert order_created is not None
    assert len(order_created.items) == 2


def test_should_fail_to_create_order_without_customer_id(client: Client):
    invalid_order = {
        "shippingAddress": "Rua Teste, 123",
        "items": [
            {
                "productId": "dcd53ddb-8104-4e48-8cc0-5df1088c6113",
                "productName": "Produto Teste",
                "quantity": 1,
                "unityPrice": 100.00,
            }
        ],
    }

    response = client.post("/orders", data=invalid_order)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_should_fail_to_create_order_without_shipping_address(client: Client):
    invalid_order = {
        "customerId": "87d8e330-2878-4742-a86f-dbbb3bf522ac",
        "items": [
            {
                "productId": "dcd53ddb-8104-4e48-8cc0-5df1088c6113",
                "productName": "Produto Teste",
                "quantity": 1,
                "unityPrice": 100.00,
            }
        ],
    }

    response = client.post("/orders", data=invalid_order)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_should_fail_to_create_order_with_invalid_customer_id(client: Client):
    invalid_order = {
        "customerId": "invalid-uuid",
        "shippingAddress": "Rua Teste, 123",
        "items": [
            {
                "productId": "dcd53ddb-8104-4e48-8cc0-5df1088c6113",
                "productName": "Produto Teste",
                "quantity": 1,
                "unityPrice": 100.00,
            }
        ],
    }

    response = client.post("/orders", data=invalid_order)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_should_find_order_by_id(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == HTTPStatus.OK
    order_data = response.json()
    assert order_data["id"] == order_id
    assert order_data["customerId"] == DEFAULT_ORDER["customerId"]
    assert order_data["shippingAddress"] == DEFAULT_ORDER["shippingAddress"]
    assert order_data["status"] == OrderStatus.CREATED.value
    assert "createdAt" in order_data
    assert "updatedAt" in order_data
    assert len(order_data["items"]) == len(DEFAULT_ORDER["items"])


def test_should_return_404_when_order_not_found(client: Client):
    non_existent_id = str(uuid4())
    response = client.get(f"/orders/{non_existent_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_should_return_422_when_order_id_is_invalid(client: Client):
    invalid_id = "invalid-uuid-format"
    response = client.get(f"/orders/{invalid_id}")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_should_update_order_status_from_created_to_processing(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")

    update_data = {"newStatus": OrderStatus.PROCESSING.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    order = fake_order_repository.find_by_id(order_id)
    assert order is not None
    assert order.status == OrderStatus.PROCESSING


def test_should_update_order_status_from_created_to_cancelled(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")

    update_data = {"newStatus": OrderStatus.CANCELLED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    order = fake_order_repository.find_by_id(order_id)
    assert order is not None
    assert order.status == OrderStatus.CANCELLED


def test_should_update_order_status_from_processing_to_shipped(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")
    client.patch(
        f"/orders/{order_id}", data={"newStatus": OrderStatus.PROCESSING.value}
    )

    update_data = {"newStatus": OrderStatus.SHIPPED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    order = fake_order_repository.find_by_id(order_id)
    assert order is not None
    assert order.status == OrderStatus.SHIPPED


def test_should_update_order_status_from_processing_to_cancelled(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")
    client.patch(
        f"/orders/{order_id}", data={"newStatus": OrderStatus.PROCESSING.value}
    )

    update_data = {"newStatus": OrderStatus.CANCELLED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    order = fake_order_repository.find_by_id(order_id)
    assert order is not None
    assert order.status == OrderStatus.CANCELLED


def test_should_update_order_status_from_shipped_to_delivered(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")
    client.patch(
        f"/orders/{order_id}", data={"newStatus": OrderStatus.PROCESSING.value}
    )
    client.patch(f"/orders/{order_id}", data={"newStatus": OrderStatus.SHIPPED.value})

    update_data = {"newStatus": OrderStatus.DELIVERED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    order = fake_order_repository.find_by_id(order_id)
    assert order is not None
    assert order.status == OrderStatus.DELIVERED


def test_should_fail_to_update_with_invalid_status_transition(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")

    update_data = {"newStatus": OrderStatus.SHIPPED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_should_fail_to_update_with_invalid_status_transition_created_to_delivered(
    client: Client,
):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")

    update_data = {"newStatus": OrderStatus.DELIVERED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_should_fail_to_update_cancelled_order(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")
    client.patch(f"/orders/{order_id}", data={"newStatus": OrderStatus.CANCELLED.value})

    update_data = {"newStatus": OrderStatus.PROCESSING.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_should_fail_to_update_delivered_order(client: Client):
    create_response = client.post("/orders", data=DEFAULT_ORDER)
    order_id = create_response.json().get("orderId")
    client.patch(
        f"/orders/{order_id}", data={"newStatus": OrderStatus.PROCESSING.value}
    )
    client.patch(f"/orders/{order_id}", data={"newStatus": OrderStatus.SHIPPED.value})
    client.patch(f"/orders/{order_id}", data={"newStatus": OrderStatus.DELIVERED.value})

    update_data = {"newStatus": OrderStatus.CANCELLED.value}
    response = client.patch(f"/orders/{order_id}", data=update_data)

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_should_fail_to_update_status_of_non_existent_order(client: Client):
    non_existent_id = str(uuid4())
    update_data = {"newStatus": OrderStatus.PROCESSING.value}
    response = client.patch(f"/orders/{non_existent_id}", data=update_data)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_should_fail_to_update_status_with_invalid_order_id(client: Client):
    invalid_id = "invalid-uuid-format"
    update_data = {"newStatus": OrderStatus.PROCESSING.value}
    response = client.patch(f"/orders/{invalid_id}", data=update_data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
