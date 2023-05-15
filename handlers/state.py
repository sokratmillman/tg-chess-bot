from aiogram.dispatcher.filters.state import State, StatesGroup

class ChessState(StatesGroup):
    AI_GAME = State()
    WAITING = State()
    PVP_GAME = State()
