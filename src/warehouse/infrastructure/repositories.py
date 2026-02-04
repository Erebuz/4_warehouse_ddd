from typing import List, Optional

from src.warehouse.domain.repository import StoragesRepository
from src.warehouse.domain.store import Storing


class InMemoryStoragesRepository(StoragesRepository):
    def __init__(self) -> None:
        self._items: dict[str, Storing] = {}

    def get(self, storing_id: str) -> Optional[Storing]:
        return self._items.get(storing_id)

    def add(self, storing: Storing) -> None:
        self._items[storing.id] = storing

    def list_all_storing(self) -> List[Storing]:
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
