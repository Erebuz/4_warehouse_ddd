from typing import List, Optional

from src.warehouse.domain.rack import Rack
from src.warehouse.domain.repository import RacksRepository, StoragesRepository
from src.warehouse.domain.store import Storing


class InMemoryStoragesRepository(StoragesRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self._items: dict[str, Storing] = {}
            self.initialized = True

    def get(self, storing_id: str) -> Optional[Storing]:
        return self._items.get(storing_id)

    def add(self, storing: Storing) -> None:
        self._items[storing.id] = storing

    def list_all_storing(self) -> List[Storing]:
        return [r for r in self._items.values()]


class InMemoryRacksRepository(RacksRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self._items: dict[str, Rack] = {}
            self.initialized = True

    def get(self, rack_id: str) -> Optional[Rack]:
        return self._items.get(rack_id)

    def add(self, rack: Rack) -> None:
        self._items[rack.id.value] = rack

    def list_all_storing(self) -> List[Rack]:
        return [r for r in self._items.values()]


# # Заготовка под SQLAlchemy (для лекции / дальнейшего расширения)
# class SqlAlchemyReservationRepository(ReservationRepository):
#     def __init__(self, session) -> None:
#         self.session = session
#
#     def get(self, reservation_id: str) -> Optional[Reservation]:
#         raise NotImplementedError
#
#     def add(self, reservation: Reservation) -> None:
#         raise NotImplementedError
#
#     def list_for_slot(self, slot: TimeSlot) -> List[Reservation]:
#         raise NotImplementedError
