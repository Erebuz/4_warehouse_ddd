from dataclasses import dataclass


@dataclass(frozen=True)
class CreateItemStoring:
    name: str
    weight: float
    width: float
    height: float
    length: float
