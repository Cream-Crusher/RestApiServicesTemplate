from typing import Any, Self

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class CKB(ReplyKeyboardMarkup):
    keyboard: list[list[KeyboardButton]] = []

    def row(
        self,
        text: str | KeyboardButton | None = None,
        **kv: Any,
    ) -> Self:
        self.keyboard.append([])

        if text:
            return self.btn(text, **kv)

        return self

    def btn(
        self,
        text: str | KeyboardButton | None = None,
        **kv: Any,
    ) -> Self:

        if isinstance(text, KeyboardButton):
            self.keyboard[-1].append(text)
            return self

        assert text is not None, "text is required"

        self.keyboard[-1].append(KeyboardButton(text=text, **kv))
        return self
