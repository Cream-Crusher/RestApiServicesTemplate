from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine

from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import use_context_value, db_session_var
from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel


class UsersContextFactory:
    user_a_id: int = 1
    user_b_id: int = 2

    user_id_for_create: int = 3
    user_id_for_update: int = 4
    user_id_for_delete: int = 5

    def __init__(self, engine, factory):
        self.engine: AsyncEngine = engine
        self.factory: async_sessionmaker[AsyncSession] = factory
        self.models: list[BaseSqlModel] = []

    async def __clear_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseSqlModel.metadata.drop_all)
            await conn.run_sync(BaseSqlModel.metadata.create_all)

    async def __aenter__(self):
        await self.__clear_db()
        self.models.extend(
            [
                User(id=self.user_a_id, first_name="first_name", last_name="last_name", username="username"),
                User(id=self.user_b_id, first_name="first_name", last_name="last_name", username="username"),
                User(id=self.user_id_for_delete, first_name="first_name", last_name="last_name", username="username"),
                User(id=self.user_id_for_update, first_name="first_name", last_name="last_name", username="username"),
            ]
        )

        async with cast(AsyncSession, self.factory()) as session:
            with use_context_value(db_session_var, session):
                for model in self.models:
                    session.add(model)

                await session.commit()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__clear_db()
