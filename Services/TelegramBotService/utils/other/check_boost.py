from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


async def check_boost(bot: Bot, user_id: str | int, tg_channel_id: str | int) -> bool:
    try:
        chat_boosts = await bot.get_user_chat_boosts(chat_id=tg_channel_id, user_id=int(user_id))
        if len(chat_boosts.boosts) != 0:
            return True

    except TelegramBadRequest:
        return False

    return False
