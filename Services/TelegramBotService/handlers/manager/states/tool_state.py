from aiogram.fsm.state import State, StatesGroup


class ToolState(StatesGroup):
    get_file_id = State()
    get_file_url = State()
    start_mallin = State()
    send_broadcast = State()
