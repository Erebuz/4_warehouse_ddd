import uuid
from dataclasses import dataclass


@dataclass
class Item:
    id: str
    name: str
    weight: float
    width: float
    height: float
    length: float

class ItemFactory:
    @staticmethod
    def create(name: str, weight: float, width: float, height: float, length: float) -> Item:
        item_id = str(uuid.uuid4())

        # Тут можно сделать проверки, но лень
        return Item(item_id, name, weight, width, height, length)