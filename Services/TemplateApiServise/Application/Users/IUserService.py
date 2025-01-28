from typing import Protocol

from Services.TemplateApiServise.Application.Users.user_dto import CreateUserDto
from Services.TemplateApiServise.Domain.User import User


class IUserService(Protocol):

    async def create(self, user: CreateUserDto) -> User:
        ...
