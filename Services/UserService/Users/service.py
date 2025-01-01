from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Services.UserService.Users.model import Users
from Shared.Base.BaseRepository import BaseRepository
from Shared.Sessions.session import AsyncDatabase


class UserRepository(BaseRepository[Users, int]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Users)


async def get_user_repository(session: AsyncSession = Depends(AsyncDatabase.get_session)):
    return UserRepository(session)


user_repository: UserRepository = Depends(get_user_repository)
