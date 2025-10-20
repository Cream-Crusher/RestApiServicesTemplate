from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def check_subscription(bot: Bot, user_id: str | int, tg_channel_id: str | int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=tg_channel_id, user_id=int(user_id))
    except TelegramBadRequest:
        return False

    return member.status in ["creator", "administrator", "member"]
