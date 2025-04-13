from aiogram.filters import Filter
from aiogram.types import Message


class ManagerFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        user_id: int = message.from_user.id  # type: ignore
        return user_id in [1001631806]
