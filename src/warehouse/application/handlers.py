from src.warehouse.application.commands import CreateItemStoring
from src.warehouse.application.unit_of_work import UnitOfWork
from src.warehouse.domain.item import ItemFactory
from src.warehouse.domain.rack import RackAggregate
from src.warehouse.domain.services import ShelfAllocationService
from src.warehouse.domain.store import StoringFactory, StoringAggregate


class CreateStoringHandler:
    def __init__(self, uow: UnitOfWork, allocator: ShelfAllocationService):
        self.uow = uow
        self.allocator = allocator

    def __call__(self, cmd: CreateItemStoring, racks: list[RackAggregate]) -> None:
        item = ItemFactory.create(cmd.name, cmd.weight, cmd.width, cmd.height, cmd.length)
        storing = StoringFactory.create(item)

        storing_agg = StoringAggregate(storing)

        rack_id, shelf_id = self.allocator.allocate(storing, racks)
        storing_agg.assign_shelf(rack_id, shelf_id)