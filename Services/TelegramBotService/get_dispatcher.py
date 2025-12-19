from functools import cache

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis
from redis.asyncio import Redis

from config import config
from Services.TelegramBotService.BotMiddlewares.UserMW import user_middleware  # type: ignore
from Services.TelegramBotService.handlers.manager.routers import flow_tool
from Services.TelegramBotService.handlers.users.routers import flow_start


@cache
def get_dispatcher() -> Dispatcher:
    redis: Redis | None = aioredis.Redis(host=config.redis_config.host) if config.redis_config.host else None
    storage: BaseStorage = MemoryStorage() if redis is None else RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    dp.message.outer_middleware(user_middleware)
    dp.callback_query.outer_middleware(user_middleware)
    dp.include_router(router=flow_start.router)
    dp.include_router(router=flow_tool.router)
    return dp
