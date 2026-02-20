from aiogram import Bot
from loguru import logger

from Services.TelegramBotService.get_bot import get_bot
from Services.TelegramBotService.get_dispatcher import get_dispatcher


async def start_polling_bot():
    bot: Bot = get_bot()
    dp = get_dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logger.info("Bot polling started")
