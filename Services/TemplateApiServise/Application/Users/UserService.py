from fastapi import Depends

from Services.TemplateApiServise.Application.Users.user_dto import CreateUserDto
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Repository.UserRepository import UserRepository, get_user_repository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    async def create(self, user: CreateUserDto) -> User:
        user_model = User(**user.model_dump())
        return await self._repository.create(user_model)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


user_service: UserService = Depends(get_user_service)
