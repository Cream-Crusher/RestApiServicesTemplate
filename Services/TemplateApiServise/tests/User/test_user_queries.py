import pytest

from Services.TemplateApiServise.Application.Users.user_dtos import GetUserByIdDTO
from Services.TemplateApiServise.WebApi.Controllers.UserController import get_user_by_id_api  # type: ignore
from Services.TemplateApiServise.tests.Common.UsersContextFactory import UsersContextFactory

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio(scope="session")
async def test_get_user_by_id(test_engine, test_factory, test_client):
     async with UsersContextFactory(test_engine, test_factory) as user_context:
        # Arrange
        user_a_id = user_context.user_a_id

        # Act
        response = await test_client.get(f"/users/{user_a_id}")

        # Assert
        assert response.status_code == 200
        assert GetUserByIdDTO(**response.json())
