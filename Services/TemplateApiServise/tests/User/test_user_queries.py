import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from Services.TemplateApiServise.Application.Users.user_dtos import GetUserByIdDTO
from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService
from Services.TemplateApiServise.tests.Common.UsersContextFactory import (
    UsersContextFactory,
)

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio(scope="session")
async def test_get_user_by_id(
    test_engine: AsyncEngine, test_factory: async_sessionmaker[AsyncSession], test_client: AsyncClient,
    test_cache_service: ModelCacheService
) -> None:
    async with UsersContextFactory(engine=test_engine, factory=test_factory,
                                   cache_service=test_cache_service) as user_context:  # type: ignore
        # Arrange
        user_a_id = user_context.user_a_id

        # Act
        response = await test_client.get(f"/users/{user_a_id}")

        # Assert
        assert response.status_code == 200
        assert GetUserByIdDTO(**response.json())
