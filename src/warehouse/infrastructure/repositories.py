from typing import Optional, List

from src.warehouse.domain.repository import StoringRepository
from src.warehouse.domain.store import Storing


class InMemoryReservationRepository(StoringRepository):
    def __init__(self) -> None:
        self._items: dict[str, Storing] = {}

    def get(self, reservation_id: str) -> Optional[Storing]:
        return self._items.get(reservation_id)

    def add(self, reservation: Storing) -> None:
        self._items[reservation.id] = reservation

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
