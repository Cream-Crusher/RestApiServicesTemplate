from aiogram.types import CallbackQuery, Message

from Services.TelegramBotService.utils.message.assert_message import assert_message


async def delete_bot_message(query: CallbackQuery | Message) -> None:
    msg = assert_message(query)
    if msg.from_user and msg.from_user.is_bot:
        await msg.delete()
