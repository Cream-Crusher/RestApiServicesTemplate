import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from Services.TemplateApiServise.Persistence.Database.DbContext import engine, factory
from Services.TemplateApiServise.WebApi.app import app, router


@pytest.fixture(scope="session")
def test_engine() -> AsyncEngine:
    return engine


@pytest.fixture(scope="session")
def test_factory() -> async_sessionmaker[AsyncSession]:
    return factory


@pytest.fixture(scope="session")
def test_client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url=f"https://test{router.prefix}")
