from aiogram.types import CallbackQuery, Message


def assert_message(query: CallbackQuery | Message) -> Message:
    if isinstance(query, CallbackQuery):
        message = query.message
        assert isinstance(message, Message)
    else:
        message = query
    return message
