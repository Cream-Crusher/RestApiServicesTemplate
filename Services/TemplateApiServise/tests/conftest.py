import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine

from Services.TemplateApiServise.Persistence.Database.DbContext import engine, factory


@pytest.fixture(scope='session')
def engine_fixture() -> AsyncEngine:
    return engine


@pytest.fixture(scope='session')
def factory_fixture() -> async_sessionmaker[AsyncSession]:
    return factory
