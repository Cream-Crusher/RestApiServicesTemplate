from typing import Generator, Any, Sequence, Callable, Iterator

from sqlalchemy import ScalarResult, Select

from Services.TemplateApiServise.Persistence.Database.DbContext import require_session


class SelectOfScalarExtended[TM](Select):
    inherit_cache = True

    def __await__(self) -> Generator[Any, Any, ScalarResult[TM]]:
        return self.exec().__await__()

    async def exec(self) -> ScalarResult[TM]:
        session = require_session()
        return await session.scalars(self)  # type: ignore

    async def all(self) -> Sequence[TM]:
        return (await self).all()

    async def all_map[T](self, callback: Callable[[TM], T]):
        return list(map(callback, await self.all()))

    async def unique(self, strategy: Any | None = None) -> ScalarResult[TM]:
        return (await self).unique(strategy)

    async def partitions(self, size: int | None = None) -> Iterator[Sequence[TM]]:
        return (await self).partitions(size)

    async def fetchall(self) -> Sequence[TM]:
        return (await self).fetchall()

    async def fetchmany(self, size: int | None = None) -> Sequence[TM]:
        return (await self).fetchmany(size)

    async def first(self) -> TM | None:
        return (await self).first()

    async def one(self) -> TM:
        return (await self).one()

    async def one_or_none(self) -> TM | None:
        return (await self).one_or_none()

    async def one_or_raise(self, exception: BaseException) -> TM:
        result = await self.one_or_none()
        if result is None:
            raise exception
        return result

    async def one_or_call[T](self, callback: Callable[[], T]) -> T | TM:
        result = await self.one_or_none()
        if result is None:
            return callback()
        return result

    async def one_or[T](self, default: T) -> T | TM:
        result = await self.one_or_none()
        if result is None:
            return default
        return result
