from datetime import datetime
from typing import Any, List

from src.warehouse.domain.events import RackCreated
from src.warehouse.domain.item import Item
from src.warehouse.domain.value_objects import RackId, ShelfArea, ShelfId


class Shelf:
    def __init__(self, shelf_id: ShelfId, area: ShelfArea):
        self.id = shelf_id
        self.area = area
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        """
        Добавляет предмет на полку с проверкой на возможность размещения

        Вызывает исключение, если предмет не проходит по каким-то параметрам.
        """
        # TODO: Реализовать проверки
        self.items.append(item)


class Rack:
    def __init__(self, rack_id: RackId, shelves: List[Shelf]):
        self.id = rack_id
        self.shelves = {s.id.value: s for s in shelves}


class RackAggregate:
    def __init__(self, rack: Rack):
        self._root = rack
        self.events: List[Any] = []

    @property
    def root(self) -> Rack:
        return self._root

    @classmethod
    def create(cls, rack_id: str, shelves: List[Shelf]) -> "RackAggregate":
        root = Rack(rack_id=RackId(value=rack_id), shelves=shelves)
        agg = cls(root)
        agg.events.append(RackCreated(rack_id, datetime.now()))
        return agg

    def get_shelf(self, shelf_id: ShelfId) -> Shelf:
        try:
            return self._root.shelves[shelf_id.value]
        except ValueError:
            raise ValueError(f"Shelf {shelf_id} does not exist in this rack ${self._root.id}")

    def store_item_on_shelf(self, item: Item, shelf_id: ShelfId) -> None:
        shelf = self.get_shelf(shelf_id)
        shelf.add_item(item)
