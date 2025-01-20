from typing import Sequence, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row, and_
from Services.UserService.Users.model import User
from Shared.Base.BaseRepository import BaseBotRepository, session_handler


class UserRepository(BaseBotRepository[User, int]):

    def __init__(self, model: type[User]) -> None:
        super().__init__(model)


UserRep: UserRepository = UserRepository(model=User)
