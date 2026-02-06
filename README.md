# Restaurant Booking (DDD + Clean Architecture)

Это учебный проект по разработке системы управления складом в использованием Domain Driven Design

## Структура
- `src/storing/domain` — доменная модель (Entity/VO/Aggregate Root), инварианты, события, доменные сервисы, порты (Repository).
- `src/storing/application` — use-cases (handlers), Unit of Work порт.
- `src/storing/infrastructure` — адаптеры (in-memory repo/uow), заготовки под SQLAlchemy.
- `src/storing/entrypoints` — пример HTTP entrypoint (FastAPI-скелет без зависимости в pyproject).


## Команды
make test - тестирование кода
make lint - запуск линтеров


## Доменные термины (Ubiquitous Language)
- Item - предмет (пакет, коробка) для хранения
- Rack - стеллаж. Стеллаж состоит из 1 или более полок
- RackId - идентификатор стеллажа
- Shelf - полка. На одну полку может быть положено несколько предметов
- ShelfId - идентификатор полки (идентификатор стеллажа + номер полки)
- ShelfArea - размер и высота полки
- Storing - запись о хранении
- StoringStatus — статус хранения
- UserId - идентификатор пользователя
