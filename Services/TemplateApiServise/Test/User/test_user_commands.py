import pytest

from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto, UpdateUserDto
from Services.TemplateApiServise.Application.common.BaseResponse import BaseResponse
from Services.TemplateApiServise.WebApi.Controllers.UserController import update_user_api, create_user_api, \
    delete_user_api

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio(scope="session")
async def test_delete_user():
    # Arrange
    user_id = 3

    # Act
    response = await delete_user_api(
        user_id,
    )

    # Assert
    assert isinstance(response, BaseResponse)
    assert response.success is True


@pytest.mark.asyncio(scope="session")
async def test_create_user():
    # Arrange
    new_user_dto = CreateUserDto(
        id=3,
        first_name="John",
        last_name="Smith",
        username="username"
    )

    # Act
    response = await create_user_api(new_user_dto)

    # Assert
    assert isinstance(response, BaseResponse)
    assert response.success is True


@pytest.mark.asyncio(scope="session")
async def test_update_user():
    # Arrange
    user_id = 3
    update_user_dto = UpdateUserDto(
        first_name="John_new",
        last_name="Smith_new",
        username="username_new"
    )

    # Act
    response = await update_user_api(
        user_id,
        update_user_dto
    )

    # Assert
    assert isinstance(response, BaseResponse)
    assert response.success is True
