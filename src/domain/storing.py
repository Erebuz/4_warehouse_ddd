from datetime import datetime

from src.domain.item import Item
from src.domain.value_objects import ShelfId, StoringStatus, UserId


class Storing:
    def __init__(self, item: Item, shelf_id: ShelfId, status: StoringStatus, user: UserId):
        """
        Запись для хранения информации об измененим статуса хранения предмета

        :param item: предмет на хранении
        :param shelf_id: идентификатор полки, где находится предмет
        :param status: статус хранения предмета
        :param user: идентификатор пользователя, внесшего запись
        """
        self.item = item
        self.shelf_id = shelf_id
        self.timestamp: datetime = datetime.now()
        self.status: StoringStatus = status
        self.user = user
