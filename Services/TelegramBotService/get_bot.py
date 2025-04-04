from functools import cache

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from config import settings


@cache
def get_bot() -> Bot:
    return Bot(
        settings.bot_config.token,
        default=DefaultBotProperties(
            parse_mode='html',
        )
    )
