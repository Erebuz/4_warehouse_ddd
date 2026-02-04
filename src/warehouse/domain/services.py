from typing import Iterable, Tuple

from src.warehouse.domain.rack import RackAggregate
from src.warehouse.domain.store import Storing
from src.warehouse.domain.value_objects import RackId, ShelfId


class ShelfAllocationService:
    def allocate(self, storing: Storing, racks: Iterable[RackAggregate]) -> Tuple[RackId, ShelfId]:
        """
        Поиск подходящей полки для хранения
        """

        # TODO: Реализовать логику поиска подходящей полки

        raise NotImplementedError