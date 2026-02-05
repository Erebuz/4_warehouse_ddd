from dataclasses import dataclass


@dataclass(frozen=True)
class CreateItemStoring:
    name: str
    weight: float
    width: float
    height: float
    length: float

@dataclass(frozen=True)
class AcceptItemStoring:
    storing_id: str
    rack_id: str
    shelf_id: int

@dataclass(frozen=True)
class PickUpItemStoring:
    storing_id: str

@dataclass(frozen=True)
class CancelledItemStoring:
    storing_id: str
