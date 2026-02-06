from src.warehouse.application.commands import (CancelItemStoring,
                                                CreateItemStoring,
                                                PickUpItemStoring)
from src.warehouse.application.unit_of_work import UnitOfWork
from src.warehouse.domain.item import ItemFactory
from src.warehouse.domain.rack import RackAggregate
from src.warehouse.domain.services import ShelfAllocationService
from src.warehouse.domain.store import StoringAggregate, StoringFactory


class BaseHandler:
    def __init__(self, uow: UnitOfWork, allocator: ShelfAllocationService):
        self.uow = uow
        self.allocator = allocator


class CreateStoringHandler(BaseHandler):
    def __call__(
        self, cmd: CreateItemStoring, racks: list[RackAggregate]
    ) -> StoringAggregate:
        item = ItemFactory.create(
            cmd.name, cmd.weight, cmd.width, cmd.height, cmd.length
        )
        storing = StoringFactory.create(item)
        storing_agg = StoringAggregate(storing)

        ids = self.allocator.allocate(storing, racks)
        if ids is None:
            raise ValueError("No suitable rack and shelf found")

        rack, shelf_id = ids

        storing_agg.assign_shelf(rack.root.id, shelf_id)
        rack.store_item_on_shelf(storing.item, shelf_id)

        with self.uow:
            self.uow.storages.add(storing_agg.root)
            self.uow.racks.update(rack.root)
            self.uow.commit()

        return storing_agg


class PickUpStoringHandler(BaseHandler):
    def __call__(self, cmd: PickUpItemStoring) -> StoringAggregate:
        with self.uow:
            storing = self.uow.storages.get(cmd.storing_id)
            storing_agg = StoringAggregate(storing)

            rack = self.uow.racks.get(storing.rack_id.value)
            rack_agg = RackAggregate(rack)

            rack_agg.remove_item_from_shelf(storing.item, storing_agg.root.shelf_id)
            storing_agg.pick_up()

            self.uow.storages.update(storing_agg.root)
            self.uow.racks.update(rack_agg.root)

            self.uow.commit()

        return storing_agg


class CancelStoringHandler(BaseHandler):
    def __call__(self, cmd: CancelItemStoring) -> StoringAggregate:
        with self.uow:
            storing = self.uow.storages.get(cmd.storing_id)
            storing_agg = StoringAggregate(storing)

            rack = self.uow.racks.get(storing.rack_id.value)
            rack_agg = RackAggregate(rack)

            rack_agg.remove_item_from_shelf(storing.item, storing_agg.root.shelf_id)
            storing_agg.cancelled()

            self.uow.storages.update(storing_agg.root)
            self.uow.racks.update(rack)

            self.uow.commit()

        return storing_agg
