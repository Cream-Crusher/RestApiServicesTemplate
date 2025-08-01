import logging
from collections.abc import Callable

from aiogram.types import Update, User
from pydantic import BaseModel


class TelegramUser(BaseModel):
    id: str | int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


async def user_middleware(
    handler: Callable, event: Update, data: dict[str, TelegramUser]  # type: ignore
) -> TelegramUser | None:  # type: ignore
    try:
        # Type assertion to help the type checker
        from_user: User = event.from_user  # type: ignore

        data["telegram_user"] = TelegramUser(
            id=from_user.id,  # type: ignore
            username=from_user.username,  # type: ignore
            first_name=from_user.first_name,  # type: ignore
            last_name=from_user.last_name,  # type: ignore
        )

        return await handler(event, data)  # type: ignore
    except Exception as e:
        logging.error(e)
        return None
