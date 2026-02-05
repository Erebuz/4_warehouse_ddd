from src.warehouse.application.commands import CreateItemStoring, AcceptItemStoring, PickUpItemStoring
from src.warehouse.application.unit_of_work import UnitOfWork
from src.warehouse.domain.item import ItemFactory
from src.warehouse.domain.rack import RackAggregate, Rack, Shelf
from src.warehouse.domain.services import ShelfAllocationService
from src.warehouse.domain.store import StoringAggregate, StoringFactory
from src.warehouse.domain.value_objects import RackId, ShelfId


class BaseHandler:
    def __init__(self, uow: UnitOfWork, allocator: ShelfAllocationService):
        self.uow = uow
        self.allocator = allocator

class CreateStoringHandler(BaseHandler):
    def __call__(self, cmd: CreateItemStoring, racks: list[RackAggregate]) -> str:
        item = ItemFactory.create(
            cmd.name, cmd.weight, cmd.width, cmd.height, cmd.length
        )
        storing = StoringFactory.create(item)

        storing_agg = StoringAggregate(storing)

        ids = self.allocator.allocate(storing, racks)
        if ids is None:
            raise ValueError("No suitable rack and shelf found")

        storing_agg.assign_shelf(*ids)

        with self.uow:
            self.uow.storages.add(storing_agg.root)
            self.uow.commit()

        return storing.id

class AcceptedStoringHandler(BaseHandler):
    def __call__(self, cmd: AcceptItemStoring):
        with self.uow:
            storing = self.uow.storages.get(cmd.storing_id)
            storing_agg = StoringAggregate(storing)
            rack = self.uow.racks.get(cmd.rack_id)
            rack_agg = RackAggregate(rack)

            storing_agg.assign_shelf(rack.id, ShelfId(cmd.shelf_id))
            rack_agg.store_item_on_shelf(storing.item, ShelfId(cmd.shelf_id))

            self.uow.storages.update(storing_agg.root)
            self.uow.racks.update(rack)

            self.uow.commit()

class PickUpStoringHandler(BaseHandler):
    def __call__(self, cmd: PickUpItemStoring):
        with self.uow:
            storing = self.uow.storages.get(cmd.storing_id)
            storing_agg = StoringAggregate(storing)

            rack = self.uow.racks.get(storing.rack_id.value)
            rack_agg = RackAggregate(rack)

            storing_agg.pick_up()
            rack_agg.remove_item_from_shelf(storing.item, storing_agg.root.shelf_id)

            self.uow.storages.update(storing_agg.root)
            self.uow.racks.update(rack)

            self.uow.commit()

class CancelStoringHandler(BaseHandler):
    def __call__(self, cmd: AcceptItemStoring):
        with self.uow:
            storing = self.uow.storages.get(cmd.storing_id)
            storing_agg = StoringAggregate(storing)

            rack = self.uow.racks.get(storing.rack_id.value)
            rack_agg = RackAggregate(rack)

            storing_agg.cancelled()
            rack_agg.remove_item_from_shelf(storing.item, storing_agg.root.shelf_id)

            self.uow.storages.update(storing_agg.root)
            self.uow.racks.update(rack)

            self.uow.commit()