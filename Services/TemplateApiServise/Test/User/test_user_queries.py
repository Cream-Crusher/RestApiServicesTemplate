import pytest

from Services.TemplateApiServise.Application.exceptions.ModelNotFound import ModelNotFound
from Services.TemplateApiServise.WebApi.Controllers.UserController import get_user_by_id_api  # type: ignore

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id_error():
    # Arrange
    user_id = 2

    # Act & Assert
    with pytest.raises(ModelNotFound):
        await get_user_by_id_api(user_id)  # type: ignore
