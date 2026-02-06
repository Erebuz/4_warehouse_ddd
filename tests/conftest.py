import pytest

from src.warehouse.application.commands import CreateItemStoring
from src.warehouse.application.handlers import CreateStoringHandler
from src.warehouse.domain.rack import RackAggregate, Shelf
from src.warehouse.domain.services import ShelfAllocationService
from src.warehouse.domain.value_objects import ShelfArea, ShelfId
from src.warehouse.infrastructure.uow import InMemoryUnitOfWork


@pytest.fixture
def created_item_and_rack():
    shelf_id = ShelfId(1)

    shelf = Shelf(shelf_id, ShelfArea(*(25, 25, 25, 25)))
    rack_agg = RackAggregate.create("RTest", [shelf])

    uow_rack = InMemoryUnitOfWork()
    uow_rack.racks.add(rack_agg.root)
    uow_rack.commit()

    uow = InMemoryUnitOfWork()
    handler = CreateStoringHandler(uow, ShelfAllocationService())
    cmd = CreateItemStoring(name="test", weight=1, width=1, height=1, length=1)

    storing_id = handler(cmd, [rack_agg])

    return rack_agg.root.id, shelf_id, storing_id
