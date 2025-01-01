from typing import Callable, Union

from aiogram.types import Update
from pydantic import BaseModel


class TelegramUser(BaseModel):
    id: str = None
    username: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


async def user_middleware(handler: Callable, event: Update, data: dict[str, TelegramUser]) -> TelegramUser:
    try:
        data['telegram_user'] = TelegramUser(
            id=event.from_user.id,
            username=event.from_user.username,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name
        )  # type: ignore

        return await handler(event, data)
    except Exception as e:
        return TelegramUser()
