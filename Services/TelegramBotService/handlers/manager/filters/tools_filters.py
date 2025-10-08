from aiogram.filters import Filter
from aiogram.types import Message

from Services.TemplateApiServise.Domain.User import User
from Services.TemplateApiServise.Persistence.Database.DbContext import get_session, transaction


class ManagerFilter(Filter):
    @transaction()
    async def __call__(self, message: Message, **kwargs) -> bool:
        get_session()
        user_id = message.from_user.id
        user: User = await User.select().where(User.id == user_id).one_or_none()
        return user and user.is_manager
