from aiogram.filters import Filter
from aiogram.types import Message


class ManagerFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        return user_id in [1001631806]
