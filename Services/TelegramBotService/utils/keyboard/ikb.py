from typing import Any, Self

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Services.TelegramBotService.utils.keyboard.cb import GlobalCallback


class IKB(InlineKeyboardMarkup):
    inline_keyboard: list[list[InlineKeyboardButton]] = []

    def row(
        self,
        text: str | InlineKeyboardButton | None = None,
        callback_data: str | CallbackData | None = None,
        **kw: Any,
    ) -> Self:
        self.inline_keyboard.append([])

        if text:
            self.btn(text=text, callback_data=callback_data, **kw)

        return self

    def btn(
        self,
        text: str | InlineKeyboardButton,
        callback_data: str | CallbackData | None = None,
        max_width: int = 300,
        **kw: Any,
    ) -> Self:

        if not self.inline_keyboard or len(self.inline_keyboard[-1]) >= max_width:
            self.row()

        if isinstance(text, InlineKeyboardButton):
            self.inline_keyboard[-1].append(text)
            return self

        if isinstance(callback_data, str):
            callback_data = GlobalCallback(data=callback_data)

        callback_data = callback_data and callback_data.pack()
        self.inline_keyboard[-1].append(InlineKeyboardButton(text=text, callback_data=callback_data, **kw))
        return self
