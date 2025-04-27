from aiogram.filters.callback_data import CallbackData


class TemplateCallBack(CallbackData, prefix="T"):
    action: str
