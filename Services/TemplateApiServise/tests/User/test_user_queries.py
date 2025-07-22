from types import coroutine
from typing import Callable, Awaitable

import pytest

from Services.TemplateApiServise.Application.Users.user_dtos import GetUserByIdDTO
from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound
from Services.TemplateApiServise.WebApi.Controllers.UserController import get_user_by_id_api  # type: ignore

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id(user_context_factory):
    # Arrange
    await user_context_factory
    user_a_id = 1

    # Act & Assert
    user = await get_user_by_id_api(user_a_id)

    assert user is not None and type(user) is GetUserByIdDTO


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id_error(user_context_factory):
    # Arrange
    await user_context_factory
    user_a_id = 2

    # Act & Assert
    with pytest.raises(ModelNotFound):
        await get_user_by_id_api(user_a_id)  # type: ignore
