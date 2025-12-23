from http import HTTPStatus
from tests.fixtures.app import Client
from tests.fixtures.repositories.fake_order_repository import fake_order_repository

DEFAULT_ORDER = {
    "customerId": "87d8e330-2878-4742-a86f-dbbb3bf522ac",
    "shippingAddress": "string",
    "items": [
        {
            "productId": "dcd53ddb-8104-4e48-8cc0-5df1088c6113",
            "productName": "string",
            "quantity": 0,
            "unityPrice": 0,
        }
    ],
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
}


def test_should_create_an_order(client: Client):
    order = fake_order_repository.find_by_id(DEFAULT_ORDER["id"])
    assert order is None
    response = client.post("/orders", data=DEFAULT_ORDER)

    assert response.status_code == HTTPStatus.CREATED
    order_id = response.json().get("orderId", "")

    order_created = fake_order_repository.find_by_id(order_id)
    assert order_created is not None
