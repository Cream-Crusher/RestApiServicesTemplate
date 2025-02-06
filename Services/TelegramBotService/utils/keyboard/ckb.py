from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class CKB(ReplyKeyboardMarkup):
    keyboard: list[list[KeyboardButton]] = []

    def row(
            self,
            text: str | KeyboardButton | None = None,
            **kv
    ):
        self.keyboard.append([])

        if text:
            return self.btn(text, **kv)

        return self

    def btn(
            self,
            text: str | KeyboardButton | None = None,
            **kv
    ):

        if isinstance(text, KeyboardButton):
            self.keyboard[-1].append(text)
            return self

        self.keyboard[-1].append(
            KeyboardButton(text=text, **kv)
        )

        return self
