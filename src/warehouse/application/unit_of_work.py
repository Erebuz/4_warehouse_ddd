from __future__ import annotations

from typing import Protocol

from src.warehouse.domain.repository import StoragesRepository


class UnitOfWork(Protocol):
    storages: StoragesRepository

    def __enter__(self) -> UnitOfWork: ...
    def __exit__(self, exc_type, exc, tb) -> None: ...

    def commit(self) -> None: ...
    def rollback(self) -> None: ...
