from aiogram.fsm.state import StatesGroup, State


class ChecksStates(StatesGroup):
    waiting = State()
