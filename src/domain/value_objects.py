from dataclasses import dataclass
from enum import Enum


class StoringStatus(Enum):
    ARRIVED = "arrived"
    STORED = "stored"
    PICKED_UP = "picked_up"
    LOST = "lost"


@dataclass(frozen=True)
class RackId:
    value: str


@dataclass(frozen=True)
class ShelfId:
    rack_id: RackId
    position: int


@dataclass(frozen=True)
class ShelfArea:
    width: float
    height: float
    length: float
    max_weight: float


@dataclass(frozen=True)
class UserId:
    value: str
