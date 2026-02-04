from dataclasses import dataclass
from enum import Enum


class StoringStatus(Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    COMPLETED = "picked_up"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class RackId:
    value: str


@dataclass(frozen=True)
class ShelfId:
    value: int


@dataclass(frozen=True)
class ShelfArea:
    width: float
    height: float
    length: float
    max_weight: float
