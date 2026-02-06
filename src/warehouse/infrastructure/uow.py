from __future__ import annotations

from types import TracebackType

from src.warehouse.application.unit_of_work import UnitOfWork
from src.warehouse.infrastructure.repositories import (
    InMemoryRacksRepository, InMemoryStoragesRepository, RedisRacksRepository,
    RedisStoragesRepository)


class InMemoryUnitOfWork(UnitOfWork):
    """UoW для тестов/демо без БД."""

    def __init__(self) -> None:
        self.storages = InMemoryStoragesRepository()
        self.racks = InMemoryRacksRepository()
        self.committed = False

    def __enter__(self) -> InMemoryUnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = False


class RedisUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self.session = None

        self.storages = RedisStoragesRepository()
        self.racks = RedisRacksRepository()
        self.committed = False

    def __enter__(self):
        self.session = self._session_factory()
        # self.reservations = SqlAlchemyReservationRepository(self.session)
        raise NotImplementedError

    def __exit__(self, exc_type, exc, tb):
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError
