from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import engine, factory, use_context_value, \
    db_session_var
from Services.TemplateApiServise.Persistence.Repository.Orm.SqlModel import BaseSqlModel


@pytest.fixture(scope="function")
async def user_context_factory():
    # Создаем и очищаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(BaseSqlModel.metadata.drop_all)
        await conn.run_sync(BaseSqlModel.metadata.create_all)

    user_a = User(id=1, first_name="first_name", last_name="last_name", username="username")
    async with cast(AsyncSession, factory()) as session:  # type: ignore
        with use_context_value(db_session_var, session):  # type: ignore
            session.add(user_a)
            await session.commit()  # type: ignore
