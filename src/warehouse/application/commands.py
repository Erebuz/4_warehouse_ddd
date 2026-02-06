from dataclasses import dataclass


@dataclass(frozen=True)
class CreateItemStoring:
    name: str
    weight: float
    width: float
    height: float
    length: float


@dataclass(frozen=True)
class PickUpItemStoring:
    storing_id: str


@dataclass(frozen=True)
class CancelItemStoring:
    storing_id: str
