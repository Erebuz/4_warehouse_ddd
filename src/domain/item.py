from dataclasses import dataclass
from uuid import UUID


@dataclass
class Item:
    id: UUID
    name: str
    weight: float
    width: float
    height: float
    length: float
    rotation_access: bool
