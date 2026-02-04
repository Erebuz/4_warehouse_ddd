from typing import Dict, List

from src.domain.item import Item
from src.domain.value_objects import RackId, ShelfArea, ShelfId


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
    def __init__(self, rack_id: RackId, shelves: Dict[int, Shelf]):
        self.id = rack_id
        self.shelves = shelves


class RackAggregate:
    def __init__(self, rack: Rack):
        self.rack = rack

    def get_shelf(self, shelf_id: ShelfId) -> Shelf:
        if self.rack.id != shelf_id.rack_id:
            raise ValueError("Shelf does not belong to this rack")

        try:
            return self.rack.shelves[shelf_id.position]
        except ValueError:
            raise ValueError("Shelf does not exist in this rack")

    def store_item_on_shelf(self, item: Item, shelf_id: ShelfId) -> None:
        shelf = self.get_shelf(shelf_id)
        shelf.add_item(item)
