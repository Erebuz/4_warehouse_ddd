from __future__ import annotations

from types import TracebackType
from typing import Protocol

from src.warehouse.domain.repository import StoragesRepository


class UnitOfWork(Protocol):
    storages: StoragesRepository

    def __enter__(self) -> UnitOfWork: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
