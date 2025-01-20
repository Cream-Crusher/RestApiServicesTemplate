from dataclasses import dataclass

from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def web_key_board(text: str, url: str) -> InlineKeyboardMarkup:
    web_app_info = WebAppInfo(url=url)

    builder = InlineKeyboardBuilder()
    builder.button(text=text, web_app=web_app_info)
    builder.adjust(1)
    return builder.as_markup()


@dataclass
class ToolKeyboardsCallbacks:
    web_kb = web_key_board
