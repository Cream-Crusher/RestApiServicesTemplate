import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from Services.TemplateApiServise.Application.common.ModelCacheService import ModelCacheService
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import (
    ModelNotFound,
)
from Services.TemplateApiServise.Application.Users.user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
)
from Services.TemplateApiServise.tests.Common.UsersContextFactory import (
    UsersContextFactory,
)
from Services.TemplateApiServise.WebApi.Controllers.UserController import get_user_by_id_api  # type: ignore

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio(scope="session")
async def test_create_user(
    test_engine: AsyncEngine,
    test_factory: async_sessionmaker[AsyncSession],
    test_client: AsyncClient,
    test_cache_service: ModelCacheService,
) -> None:
    async with UsersContextFactory(
        engine=test_engine, factory=test_factory, cache_service=test_cache_service
    ) as user_context:  # type: ignore
        # Arrange
        new_user_dto = CreateUserDTO(
            id=user_context.user_id_for_create,
            first_name="John",
            last_name="Smith",
            username="username",
        )

        # Act
        response = await test_client.post("/users", json=new_user_dto.model_dump())

        # Assert
        assert response.status_code == 201
        assert response.json()["success"] is True
        assert await get_user_by_id_api(user_context.user_id_for_create)  # type: ignore


@pytest.mark.asyncio(scope="session")
async def test_update_user(
    test_engine: AsyncEngine,
    test_factory: async_sessionmaker[AsyncSession],
    test_client: AsyncClient,
    test_cache_service: ModelCacheService,
) -> None:
    async with UsersContextFactory(
        engine=test_engine, factory=test_factory, cache_service=test_cache_service
    ) as user_context:  # type: ignore
        # Arrange
        user_id_for_update = user_context.user_id_for_update
        update_user_dto = UpdateUserDTO(first_name="John_new", last_name="Smith_new", username="username_new")

        # Act
        response = await test_client.put(f"/users/{user_id_for_update}", json=update_user_dto.model_dump())
        # Assert

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert (await get_user_by_id_api(user_id_for_update)).first_name == update_user_dto.first_name  # type: ignore


@pytest.mark.asyncio(scope="session")
async def test_delete_user(
    test_engine: AsyncEngine,
    test_factory: async_sessionmaker[AsyncSession],
    test_client: AsyncClient,
    test_cache_service: ModelCacheService,
) -> None:
    async with UsersContextFactory(
        engine=test_engine, factory=test_factory, cache_service=test_cache_service
    ) as user_context:  # type: ignore
        # Arrange
        user_id_for_delete = user_context.user_id_for_delete

        # Act
        response: Response = await test_client.delete(f"/users/{user_id_for_delete}")

        # Assert
        assert response.status_code == 200
        assert response.json()["success"] is True
        with pytest.raises(ModelNotFound):
            await get_user_by_id_api(user_id_for_delete)  # type: ignore
