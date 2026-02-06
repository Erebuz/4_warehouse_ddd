import pickle
from typing import List, Optional

import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

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



class RedisStoragesRepository(StoragesRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized = True

            retry = Retry(ExponentialBackoff(), retries=3)

            self.r = redis.Redis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=False,
                retry=retry,
                retry_on_timeout=True,
                retry_on_error=[ConnectionError, TimeoutError],
                health_check_interval=30,
                socket_timeout=5,
                socket_connect_timeout=5,
            )

    def get(self, storing_id: str) -> Optional[Storing]:
        return self.r.get('storages:' + storing_id)

    def add(self, storing: Storing) -> None:
        self.r.set('storages:' + storing.id, pickle.dumps(storing))

    def list_all_storing(self) -> List[Storing]:
        return [pickle.loads(self.r.get(key)) for key in self.r.scan_iter(match='storages:')]


class RedisRacksRepository(RacksRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized = True

            retry = Retry(ExponentialBackoff(), retries=3)

            self.r = redis.Redis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=False,
                retry=retry,
                retry_on_timeout=True,
                retry_on_error=[ConnectionError, TimeoutError],
                health_check_interval=30,
                socket_timeout=5,
                socket_connect_timeout=5,
            )

    def get(self, storing_id: str) -> Optional[Storing]:
        return self.r.get('storages:' + storing_id)

    def add(self, rack: Rack) -> None:
        self.r.set('storages:' + rack.id.value, pickle.dumps(rack))

    def list_all_storing(self) -> List[Storing]:
        return [pickle.loads(self.r.get(key)) for key in self.r.scan_iter(match='storages:')]