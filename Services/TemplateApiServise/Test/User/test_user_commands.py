from fastapi.testclient import TestClient

from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto, UpdateUserDto
from Services.TemplateApiServise.WebApi.app import router, app

client = TestClient(app)


def test_create_user():
    # Arrange
    new_user_dto = CreateUserDto(
        id=3,
        first_name="John",
        last_name="Doe",
        username="johndoe",
    )

    # Act
    response = client.post(f"{router.prefix}/users", json=new_user_dto.model_dump())

    # Assert
    assert response.status_code == 201
    assert response.json()["success"] is True


def test_update_user():
    # Arrange
    user_id = 2
    update_user_dto = UpdateUserDto(
        first_name="John_updated",
        last_name="Doe_updated",
        username="johndoe_updated",
    )

    # Act
    response = client.put(f"{router.prefix}/users/{user_id}", json=update_user_dto.model_dump())

    # Assert
    assert response.status_code == 200
    assert response.json()["success"] is True


# todo дописать тесты на удаление
# todo дописать Arrange для бд => создать моки в базе
