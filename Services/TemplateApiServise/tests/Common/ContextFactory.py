from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.sql.schema import Table

from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService
from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel

skip_tables: list[str] = [
    "alembic_version",
]

tables_to_drop: list[Table] = [table for table in BaseSqlModel.metadata.sorted_tables if table.name not in skip_tables]


class ContextFactory:

    def __init__(
        self, engine: AsyncEngine, factory: async_sessionmaker[AsyncSession], cache_service: ModelCacheService
    ) -> None:
        self.engine: AsyncEngine = engine
        self.factory: async_sessionmaker[AsyncSession] = factory
        self.cache_service: ModelCacheService = cache_service

    async def _clear_db(self):
        async with self.engine.begin() as conn:
            for table in tables_to_drop:
                await conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))

            # await conn.run_sync(BaseSqlModel.metadata.drop_all, tables=tables_to_drop)
            # не подойдет из за CASCADE. И его нестройка не поможет т к он удаляет саму модельку, а не поля.
            await conn.run_sync(BaseSqlModel.metadata.create_all)

    async def __aenter__(self) -> "ContextFactory":
        await self._clear_db()
        await self.cache_service.cache.flushall()  # type: ignore
        return self

    async def __aexit__(self, *args, **kwargs):  # type: ignore
        await self.cache_service.cache.flushall()  # type: ignore
        await self._clear_db()
