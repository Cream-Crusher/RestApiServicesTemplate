from aiogram.fsm.state import State, StatesGroup


class ToolState(StatesGroup):
    tool = State()
    start_mallin = State()
    send_broadcast = State()
