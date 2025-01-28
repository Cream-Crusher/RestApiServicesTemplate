from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.sqlalchemy_session import AsyncDatabase
from Services.TemplateApiServise.Persistence.Repository.BaseSqlAlchemyRepository import BaseSqlAlchemyRepository


class UserRepository(BaseSqlAlchemyRepository[User, int]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model=User)


async def get_user_repository(session: AsyncSession = Depends(AsyncDatabase.get_session)):
    return UserRepository(session)


get_user_rep: get_user_repository = Depends(get_user_repository)
