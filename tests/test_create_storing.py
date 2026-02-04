import pytest

from src.warehouse.application.commands import CreateItemStoring
from src.warehouse.application.handlers import CreateStoringHandler
from src.warehouse.domain.rack import RackAggregate, Shelf
from src.warehouse.domain.services import ShelfAllocationService
from src.warehouse.domain.value_objects import ShelfArea, ShelfId
from src.warehouse.infrastructure.uow import InMemoryUnitOfWork


@pytest.fixture
def uow():
    return InMemoryUnitOfWork()


class TestStoring:
    def test_create_storing(self, uow):
        handler = CreateStoringHandler(uow, ShelfAllocationService())

        cmd = CreateItemStoring(name="test", weight=1, width=1, height=1, length=1)

        rack_agg = RackAggregate.create("R1", [Shelf(ShelfId(1), ShelfArea(10, 10, 10, 10))])

        storing_id = handler(cmd, [rack_agg])

        assert storing_id
        assert uow.committed is True

        saved = uow.storages.get(storing_id)
        assert saved is not None
        assert saved.status.value == "accepted"
        assert saved.rack_id.value == "R1"
        assert saved.shelf_id.value == 1