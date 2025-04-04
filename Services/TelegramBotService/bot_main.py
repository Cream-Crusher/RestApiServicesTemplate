import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis
from aiogram.fsm.storage.memory import MemoryStorage
from functools import cache
from Services.TelegramBotService.BotMiddlewares.UserMW import user_middleware
from Services.TelegramBotService.get_bot import get_bot
from Services.TelegramBotService.handlers.manager.routers import flow_tool
from Services.TelegramBotService.handlers.users.routers import flow_start
from config import settings


async def bot_main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = get_bot()
    redis = aioredis.Redis(host=settings.redis_config.host)
    dp = Dispatcher(storage=MemoryStorage() if settings.redis_config.disable else RedisStorage(redis))

    dp.message.outer_middleware(user_middleware)  # type: ignore
    dp.callback_query.outer_middleware(user_middleware)  # type: ignore
    dp.include_router(flow_start.router)
    dp.include_router(flow_tool.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(bot_main())
