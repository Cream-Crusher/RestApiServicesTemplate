from typing import ClassVar
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.magic_filter import MagicFilter


class AutoCallback[T]:
    def __init__(self, type: type[T], **kwargs) -> None:
        self.type = type
        self.kwargs = kwargs

    def __get__(self, *_):
        return self.value

    def __set_name__(self, owner: type, name: str):
        self.value = self.type(data=name, **self.kwargs)  # type: ignore


class AutoCallbackFactory:
    def __get__[T](self, owner: None, type: type[T]):
        return AutoCallback(type)


class GlobalCallback(CallbackData, prefix="g"):
    AUTO: ClassVar = AutoCallbackFactory()

    data: str

    def filter(self, rule: MagicFilter | None = None):
        if rule is None:
            rule = F.data == self.data
        else:
            rule &= F.data == self.data
        return super().filter(rule)


class CB:
    support = GlobalCallback.AUTO
