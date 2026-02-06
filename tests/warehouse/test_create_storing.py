from contextlib import nullcontext as does_not_raise

import pytest
from _pytest.raises import RaisesExc

from src.warehouse.application.commands import (CancelItemStoring,
                                                CreateItemStoring,
                                                PickUpItemStoring)
from src.warehouse.application.handlers import (CancelStoringHandler,
                                                CreateStoringHandler,
                                                PickUpStoringHandler)
from src.warehouse.domain.rack import RackAggregate, Shelf
from src.warehouse.domain.services import ShelfAllocationService
from src.warehouse.domain.value_objects import ShelfArea, ShelfId
from src.warehouse.infrastructure.uow import InMemoryUnitOfWork


class TestStoring:
    def test_create_storing(self):
        uow = InMemoryUnitOfWork()
        handler = CreateStoringHandler(uow, ShelfAllocationService())

        cmd = CreateItemStoring(name="test", weight=1, width=1, height=1, length=1)

        rack_agg = RackAggregate.create(
            "RTest", [Shelf(ShelfId(1), ShelfArea(10, 10, 10, 10))]
        )
        storing_id = handler(cmd, [rack_agg])

        assert storing_id
        assert uow.committed is True

        saved = uow.storages.get(storing_id.root.id)

        assert saved is not None
        assert saved.status.value == "accepted"

        assert saved.rack_id is not None
        assert saved.rack_id.value == "RTest"

        assert saved.shelf_id is not None
        assert saved.shelf_id.value == 1

    @pytest.mark.parametrize(
        "shelf, items, expected",
        [
            (
                (35, 35, 35, 35),
                [("item_1", 10, 10, 10, 10), ("item_2", 20, 20, 20, 20)],
                does_not_raise(),
            ),
            (
                (15, 15, 15, 15),
                [("item_1", 10, 10, 10, 10), ("item_2", 20, 20, 20, 20)],
                RaisesExc(ValueError),
            ),
        ],
    )
    def test_find_shelf(self, shelf, items, expected) -> None:
        uow_1 = InMemoryUnitOfWork()
        uow_2 = InMemoryUnitOfWork()

        handler_1 = CreateStoringHandler(uow_1, ShelfAllocationService())
        handler_2 = CreateStoringHandler(uow_2, ShelfAllocationService())

        cmd_item_1 = CreateItemStoring(*items[0])
        cmd_item_2 = CreateItemStoring(*items[1])

        shelf = Shelf(ShelfId(1), ShelfArea(*shelf))
        rack_agg = RackAggregate.create("RTest", [shelf])

        with expected:
            storing_id_1 = handler_1(cmd_item_1, [rack_agg])
            assert uow_1.committed is True

            saved_1 = uow_1.storages.get(storing_id_1.root.id)
            assert saved_1 is not None
            assert saved_1.status.value == "accepted"

            storing_id_2 = handler_2(cmd_item_2, [rack_agg])
            assert uow_2.committed is True

            saved_2 = uow_2.storages.get(storing_id_2.root.id)
            assert saved_2 is not None
            assert saved_2.status.value == "accepted"

            assert uow_1.storages.get(storing_id_1.root.id) is not None
            assert uow_1.storages.get(storing_id_2.root.id) is not None

    def test_pick_up_storing(self, created_item_and_rack):
        rack_id, shelf_id, storing = created_item_and_rack

        uow = InMemoryUnitOfWork()
        handler_accept = PickUpStoringHandler(uow, ShelfAllocationService())

        with does_not_raise():
            storing_agg = handler_accept(PickUpItemStoring(storing.root.id))

        rack = uow.racks.get(rack_id.value)
        rack_agg = RackAggregate(rack)

        assert storing_agg.root.item not in rack_agg.get_shelf(shelf_id).items

    def test_cancel_storing(self, created_item_and_rack):
        rack_id, shelf_id, storing = created_item_and_rack

        uow = InMemoryUnitOfWork()
        handler_accept = CancelStoringHandler(uow, ShelfAllocationService())
        cmd_cancel = CancelItemStoring(storing.root.id)

        with does_not_raise():
            handler_accept(cmd_cancel)
