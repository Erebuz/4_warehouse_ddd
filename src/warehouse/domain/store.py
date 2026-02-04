import uuid
from datetime import datetime
from typing import Any, List

from src.warehouse.domain.events import (
    StorageAccepted,
    StorageCancelled,
    StorageCompleted,
    StorageCreated,
)
from src.warehouse.domain.item import Item
from src.warehouse.domain.value_objects import RackId, ShelfId, StoringStatus


class Storing:
    def __init__(self, storing_id: str, item: Item, rack_id: RackId | None = None, shelf_id: ShelfId | None = None, status: StoringStatus = StoringStatus.CREATED):
        self.id = storing_id
        self.item = item
        self.rack_id = rack_id
        self.shelf_id = shelf_id
        self.status = StoringStatus.CREATED


class StoringFactory:
    @staticmethod
    def create(item: Item) -> Storing:
        storing_id = str(uuid.uuid4())
        return Storing(storing_id, item)


class StoringAggregate:
    def __init__(self, storing: Storing) -> None:
        self._root = storing
        self.status: StoringStatus = StoringStatus.CREATED
        self.events: List[Any] = []

    @property
    def root(self) -> Storing:
        return self._root

    @classmethod
    def create(cls, storing_id: str, item: Item) -> "StoringAggregate":
        root = Storing(storing_id, item)
        agg = cls(root)
        agg.events.append(StorageCreated(storing_id, datetime.now()))
        return agg

    def assign_shelf(self, rack_id: RackId, shelf_id: ShelfId) -> None:
        if self._root.status != StoringStatus.CREATED:
            raise ValueError("Invariant: can assign shelf only for CREATED status")

        self._root.rack_id = rack_id
        self._root.shelf_id = shelf_id
        self._root.status = StoringStatus.ACCEPTED
        self.events.append(StorageAccepted(self._root.id, shelf_id.value, datetime.now()))

    def pick_up(self) -> None:
        if self._root.status != StoringStatus.ACCEPTED:
            raise ValueError("Invariant: can pick up only for ACCEPTED status")

        self._root.status = StoringStatus.COMPLETED
        self._root.shelf_id = None
        self._root.rack_id = None
        self.events.append(StorageCompleted(self._root.id, datetime.now()))

    def cancelled(self) -> None:
        if self._root.status == StoringStatus.COMPLETED:
            raise ValueError("Invariant: cannot cancel COMPLETED status")

        if self._root.status == StoringStatus.CANCELLED:
            return

        self._root.status = StoringStatus.CANCELLED
        self._root.shelf_id = None
        self._root.rack_id = None
        self.events.append(StorageCancelled(self._root.id, datetime.now()))
