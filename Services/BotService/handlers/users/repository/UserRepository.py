from typing import Sequence, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row, and_
from Services.UserService.Users.model import Users
from Shared.Base.BaseRepository import BaseBotRepository, session_handler


class UserRepository(BaseBotRepository[Users, int]):

    def __init__(self, model: type[Users]) -> None:
        super().__init__(model)


UserRep: UserRepository = UserRepository(model=Users)
