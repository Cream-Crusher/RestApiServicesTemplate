from aiogram import Bot


async def check_subscription(bot: Bot, user_id: str | int, tg_channel_id: str | int) -> bool:
    member = await bot.get_chat_member(chat_id=tg_channel_id, user_id=int(user_id))

    return True if member.status in ["creator", "administrator", "member"] else False
