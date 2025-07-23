from typing import Any, ClassVar

from aiogram import F
from aiogram.filters.callback_data import CallbackData, CallbackQueryFilter
from aiogram.utils.magic_filter import MagicFilter


class AutoCallback[T]:
    value: T

    def __init__(self, type: type[T], **kwargs: Any) -> None:
        self.type: type[T] = type
        self.kwargs: dict[str, Any] = kwargs

    def __get__(self, *_) -> T:
        return self.value

    def __set_name__(self, owner: type, name: str) -> None:
        self.value = self.type(data=name, **self.kwargs)  # type: ignore


class AutoCallbackFactory:
    def __get__[T](self, owner: None, type: type[T]) -> AutoCallback[T]:
        return AutoCallback(type=type)


class GlobalCallback(CallbackData, prefix="g"):
    AUTO: ClassVar = AutoCallbackFactory()

    data: str

    def filter(self, rule: MagicFilter | None = None) -> CallbackQueryFilter:  # type: ignore
        if rule is None:
            rule = F.data == self.data
        else:
            rule &= F.data == self.data
        return super().filter(rule=rule)


class CB:
    support: AutoCallback[GlobalCallback] = GlobalCallback.AUTO
