from aiogram import Bot, types
from aiogram.types import CallbackQuery, Message
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


def assert_message(query: CallbackQuery | Message) -> Message:
    if isinstance(query, CallbackQuery):
        message = query.message
        assert isinstance(message, Message)
    else:
        message = query
    return message


async def delete_bot_message(query: CallbackQuery | Message) -> None:
    msg = assert_message(query)
    if msg.from_user and msg.from_user.is_bot:
        await msg.delete()


async def check_subscription(bot: Bot, user_id: str | int, tg_channel_id: str | int) -> bool | AssertionError:
    member = await bot.get_chat_member(chat_id=tg_channel_id, user_id=user_id)
    assert member.status in ["creator", "administrator", "member"]

    return True
