from pytest import fixture
from mockito import when, unstub

from infra.repositories import OrdersRepository
from tests.fixtures.repositories.fake_order_repository import fake_order_repository


@fixture(scope="function", autouse=True)
def mock_fake_order_repository():
    when(OrdersRepository).save(...).thenAnswer(fake_order_repository.save)
    when(OrdersRepository).find_by_id(...).thenAnswer(fake_order_repository.find_by_id)
    when(OrdersRepository).update_status(...).thenAnswer(
        fake_order_repository.update_status
    )

    yield
    fake_order_repository.clear_data()
    unstub()
