from aiogram.types import CallbackQuery, Message
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


def assert_message(query: CallbackQuery | Message):
    if isinstance(query, CallbackQuery):
        message = query.message
        assert isinstance(message, Message)
    else:
        message = query
    return message


async def delete_bot_message(query: CallbackQuery | Message):
    msg = assert_message(query)
    if msg.from_user and msg.from_user.is_bot:
        await msg.delete()
