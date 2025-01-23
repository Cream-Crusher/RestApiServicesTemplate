from typing import Type

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from Services.UserService.Users.model import User
from Shared.Base.BaseSqlAlchemyRepository import BaseSqlAlchemyTransactionRepository


class UserRepository(BaseSqlAlchemyTransactionRepository[User, int]):

    def __init__(self, model: type[User]) -> None:
        super().__init__(model)


UserRep = UserRepository(model=User)
