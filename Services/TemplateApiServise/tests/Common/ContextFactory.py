from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.sql.schema import Table

from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel

skip_tables: list[str] = [
    "alembic_version",
]

tables_to_drop: list[Table] = [table for table in BaseSqlModel.metadata.sorted_tables if table.name not in skip_tables]


class ContextFactory:

    def __init__(self, engine: AsyncEngine, factory: async_sessionmaker[AsyncSession]) -> None:
        self.engine: AsyncEngine = engine
        self.factory: async_sessionmaker[AsyncSession] = factory

    async def _clear_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseSqlModel.metadata.drop_all, tables=tables_to_drop)
            await conn.run_sync(BaseSqlModel.metadata.create_all)

    async def __aenter__(self) -> "ContextFactory":
        await self._clear_db()
        return self

    async def __aexit__(self):
        await self._clear_db()
