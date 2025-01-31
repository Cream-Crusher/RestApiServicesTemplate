from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.TemplateApiServise.Application.Users.user_dtos import CreateUserDto
from Services.TemplateApiServise.Application.common.BaseServise import BaseServise
from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import db_context


class UserService[T, I](BaseServise):
    def __init__(
            self,
            db_context: AsyncSession
    ):
        super().__init__(db_context=db_context)

    async def create(self, user: CreateUserDto) -> User:
        user_model = User(**user.model_dump())
        self.add(user_model)
        await self.db_context.commit()

        return user_model


async def get_user_service(db_context_session: AsyncSession = Depends(db_context.get_session)):
    return UserService(db_context_session)


user_service: UserService[User, int] = Depends(get_user_service)
