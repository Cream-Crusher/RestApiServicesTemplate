from fastapi.testclient import TestClient

from Services.TemplateApiServise.Application.Users.user_dtos import GetUserByIdDTO
from Services.TemplateApiServise.WebApi.app import app, router

client = TestClient(app)


def test_get_user_by_id():
    # Arrange
    user_id = 1

    # Act
    response = client.get(f"{router.prefix}/users/{user_id}")

    # Assert
    assert response.status_code == 200
    GetUserByIdDTO(**response.json())
