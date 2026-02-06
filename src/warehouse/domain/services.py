from typing import Iterable, List, Tuple

from src.warehouse.domain.item import Item
from src.warehouse.domain.rack import RackAggregate
from src.warehouse.domain.store import Storing
from src.warehouse.domain.value_objects import ShelfArea, ShelfId


class ShelfAllocationService:
    @staticmethod
    def can_fit_item(
        new_item: Item, existing_items: List[Item], area: ShelfArea
    ) -> bool:
        """
        Проверяет, можно ли разместить новый предмет на полке с учетом существующих.
        """

        # По весу
        current_weight = sum(item.weight for item in existing_items)
        if current_weight + new_item.weight > area.max_weight:
            return False

        # По наибольшему габариту
        item_dims = sorted([new_item.width, new_item.height, new_item.length])
        area_dims = sorted([area.width, area.height, area.length])

        for i in range(3):
            if item_dims[i] > area_dims[i]:
                return False  # Предмет физически шире/длиннее/выше чем полка

        # По объему
        current_volume = sum(item.volume for item in existing_items)
        if current_volume + new_item.volume > area.volume:
            return False

        return True

    def allocate(
        self, storing: Storing, racks: Iterable[RackAggregate]
    ) -> Tuple[RackAggregate, ShelfId] | None:
        """
        Поиск подходящей полки для хранения
        """

        for rack in racks:
            for shelf in rack.shelves:
                is_suitable = self.can_fit_item(storing.item, shelf.items, shelf.area)

                if is_suitable:
                    return rack, shelf.id

        return None
