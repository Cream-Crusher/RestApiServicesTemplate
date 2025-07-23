from typing import cast

import pytest

from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto, UpdateUserDto
from Services.TemplateApiServise.Application.common.BaseResponse import BaseResponse
from Services.TemplateApiServise.WebApi.Controllers.UserController import update_user_api, create_user_api, \
    delete_user_api, get_user_by_id_api  # type: ignore
from Services.TemplateApiServise.tests.Common.UsersContextFactory import UsersContextFactory

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio(scope="session")
async def test_create_user(engine_fixture, factory_fixture):
    async with UsersContextFactory(engine_fixture, factory_fixture) as user_context:
        # Arrange
        new_user_dto = CreateUserDto(
            id=user_context.user_id_for_create,
            first_name="John",
            last_name="Smith",
            username="username"
        )

        # Act
        response: BaseResponse = cast(BaseResponse, await create_user_api(new_user_dto))  # type: ignore

        # Assert
        assert isinstance(response, BaseResponse)
        assert response.success is True
        assert (await get_user_by_id_api(user_context.user_id_for_create))


@pytest.mark.asyncio(scope="session")
async def test_update_user(engine_fixture, factory_fixture):
    async with UsersContextFactory(engine_fixture, factory_fixture) as user_context:
        # Arrange
        user_id_for_update = user_context.user_id_for_update
        update_user_dto = UpdateUserDto(
            first_name="John_new",
            last_name="Smith_new",
            username="username_new"
        )

        # Act
        response: BaseResponse = cast(BaseResponse, await update_user_api(user_id_for_update, update_user_dto))  # type: ignore

        # Assert
        assert isinstance(response, BaseResponse)
        assert response.success is True
        assert (await get_user_by_id_api(user_id_for_update)).first_name == update_user_dto.first_name


@pytest.mark.asyncio(scope="session")
async def test_delete_user(engine_fixture, factory_fixture):
    async with UsersContextFactory(engine_fixture, factory_fixture) as user_context:
        # Arrange
        user_id_for_delete = user_context.user_id_for_delete

        # Act
        response: BaseResponse = cast(BaseResponse, await delete_user_api(user_id_for_delete))  # type: ignore

        # Assert
        assert isinstance(response, BaseResponse)
        assert response.success is True
