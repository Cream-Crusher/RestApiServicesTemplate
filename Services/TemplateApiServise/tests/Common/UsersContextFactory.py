from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import (
    db_session_var,
    use_context_value,
)
from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel
from Services.TemplateApiServise.tests.Common.ContextFactory import ContextFactory


class UsersContextFactory(ContextFactory):
    user_a_id: int = 1
    user_b_id: int = 2

    user_id_for_create: int = 3
    user_id_for_update: int = 4
    user_id_for_delete: int = 5
    def __init__(self, engine: AsyncEngine, factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(engine, factory)
        self.models: list[BaseSqlModel] = []

    async def __aenter__(self) -> "UsersContextFactory":
        await self._clear_db()
        self.models.extend(
            [
                User(
                    id=self.user_a_id,
                    first_name="first_name",
                    last_name="last_name",
                    username="username",
                ),
                User(
                    id=self.user_b_id,
                    first_name="first_name",
                    last_name="last_name",
                    username="username",
                ),
                User(
                    id=self.user_id_for_delete,
                    first_name="first_name",
                    last_name="last_name",
                    username="username",
                ),
                User(
                    id=self.user_id_for_update,
                    first_name="first_name",
                    last_name="last_name",
                    username="username",
                ),
            ]
        )

        async with self.factory() as session:
            with use_context_value(db_session_var, session):
                for model in self.models:
                    session.add(model)

                await session.commit()

        return self

    async def __aexit__(self):
        await self._clear_db()
