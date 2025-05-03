from typing import Generator, Any, Sequence, Callable, Iterator, Tuple

from sqlalchemy import ScalarResult, Select
from sqlalchemy.ext.asyncio.session import AsyncSession

from Services.TemplateApiServise.Persistence.Database.DbContext import require_session


class SQLAlchemyRepository[TM](Select[Tuple[TM]]):
    inherit_cache = True

    def __await__(self) -> Generator[Any, Any, ScalarResult[TM]]:
        return self.exec().__await__()

    async def exec(self) -> ScalarResult[TM]:
        session: AsyncSession = require_session()
        return await session.scalars(statement=self)  # type: ignore

    async def all(self) -> Sequence[TM]:
        return (await self).all()

    async def all_map[T](self, callback: Callable[[TM], T]) -> list[T]:
        return list(map(callback, await self.all()))

    async def unique(self, strategy: Any | None = None) -> ScalarResult[TM]:
        return (await self).unique(strategy=strategy)

    async def partitions(self, size: int | None = None) -> Iterator[Sequence[TM]]:
        return (await self).partitions(size=size)

    async def fetchall(self) -> Sequence[TM]:
        return (await self).fetchall()

    async def fetchmany(self, size: int | None = None) -> Sequence[TM]:
        return (await self).fetchmany(size=size)

    async def first(self) -> TM | None:
        return (await self).first()

    async def first_or_raise(self, exception: BaseException) -> TM:
        result: TM | None = await self.first()
        if result is None:
            raise exception  # /NOSONAR
        return result

    async def first_or_none(self) -> TM | None:
        result: TM | None = await self.first()
        if result is None:
            return None
        return result

    async def one(self) -> TM:
        return (await self).one()

    async def one_or_none(self) -> TM | None:
        return (await self).one_or_none()

    async def one_or_raise(self, exception: BaseException) -> TM:
        result: TM | None = await self.one_or_none()
        if result is None:
            raise exception  # /NOSONAR
        return result

    async def one_or_call[T](self, callback: Callable[[], T]) -> T | TM:
        result: TM | None = await self.one_or_none()
        if result is None:
            return callback()
        return result

    async def one_or[T](self, default: T) -> T | TM:
        result: TM | None = await self.one_or_none()
        if result is None:
            return default
        return result
