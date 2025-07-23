from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from loguru import logger
from redis import asyncio as aioredis
from redis.asyncio import Redis

from config import settings
from Services.TelegramBotService.BotMiddlewares.UserMW import (
    user_middleware,  # type: ignore
)
from Services.TelegramBotService.get_bot import get_bot
from Services.TelegramBotService.handlers.manager.routers import flow_tool
from Services.TelegramBotService.handlers.users.routers import flow_start


async def bot_main():
    bot: Bot = get_bot()
    redis: Redis | None = aioredis.Redis(host=settings.redis_config.host) if settings.redis_config.host else None
    storage: BaseStorage = MemoryStorage() if redis is None else RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    dp.message.outer_middleware(user_middleware)  # type: ignore
    dp.callback_query.outer_middleware(user_middleware)  # type: ignore
    dp.include_router(router=flow_start.router)
    dp.include_router(router=flow_tool.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # type: ignore
    logger.info("Bot started")
