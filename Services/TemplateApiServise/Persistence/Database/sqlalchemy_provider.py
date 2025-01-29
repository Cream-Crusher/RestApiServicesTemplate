import logging

import sqlalchemy.engine.url as SQURL
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from Services.TemplateApiServise.WebApi.config import settings

Database = settings.database_config


class AsyncSqlalchemyProvider:
    def __init__(self, url: SQURL.URL):
        self.URL = url
        self.engine = create_async_engine(self.URL, pool_size=10, max_overflow=5)
        self.factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def get_url(self):
        return str(self.URL)

    def get_session_maker(self) -> async_sessionmaker:
        return self.factory

    async def get_session(self) -> AsyncSession:
        async with self.factory() as session:
            try:
                yield session
            except exc.SQLAlchemyError as error:
                logging.error(error)
                await session.rollback()
                raise

    async def return_session(self) -> AsyncSession:
        return self.factory()


AsyncDatabase: AsyncSqlalchemyProvider = AsyncSqlalchemyProvider(
    url=SQURL.URL.create(
        drivername="postgresql+asyncpg",
        username=Database.user,
        password=Database.password,
        host=Database.host,
        port=Database.port,
        database=Database.database
    )
)
