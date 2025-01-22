from aiogram import Bot


async def check_subscription(bot: Bot, user_id: str | int, tg_channel_id: str | int) -> bool | AssertionError:
    member = await bot.get_chat_member(chat_id=tg_channel_id, user_id=user_id)
    assert member.status in ["creator", "administrator", "member"]

    return True
