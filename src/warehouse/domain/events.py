from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StorageCreated:
    item_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class StorageAccepted:
    item_id: str
    shelf_id: int
    occurred_at: datetime


@dataclass(frozen=True)
class StorageCompleted:
    item_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class StorageCancelled:
    item_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class RackCreated:
    rack_id: str
    occurred_at: datetime
