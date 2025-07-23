import pytest

from Services.TemplateApiServise.Application.Users.user_dtos import GetUserByIdDTO
from Services.TemplateApiServise.WebApi.Controllers.UserController import get_user_by_id_api  # type: ignore
from Services.TemplateApiServise.tests.Common.UsersContextFactory import UsersContextFactory

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio(scope="session")
async def test_get_user_by_id(engine_fixture, factory_fixture):
     async with UsersContextFactory(engine_fixture, factory_fixture) as user_context:
        # Arrange
        user_a_id = user_context.user_a_id

        # Act
        user = await get_user_by_id_api(user_a_id)

        # Assert
        assert user is not None and isinstance(user, GetUserByIdDTO)
