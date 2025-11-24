from functools import cache

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import LinkPreviewOptions

from config import settings


@cache
def get_bot() -> Bot:
    return Bot(
        settings.bot_config.token,
        default=DefaultBotProperties(
            link_preview_is_disabled=True,
            link_preview_prefer_small_media=False,
            link_preview_prefer_large_media=True,
            link_preview_show_above_text=False,
            parse_mode="html",
            link_preview=LinkPreviewOptions(
                is_disabled=True,
            ),
        ),
    )
