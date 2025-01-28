from dataclasses import dataclass

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


mailing_confirmation_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="yes"), KeyboardButton(text="no")]],
    resize_keyboard=True,
    one_time_keyboard=True
)


@dataclass
class ToolKeyboardsCommands:
    mailing_confirmation_kb = mailing_confirmation_keyboard
