from aiogram.dispatcher.filters.state import StatesGroup, State


class ADD_XODIM_state(StatesGroup):
    ism_familiya = State()
    lavozimi = State()
    tel_nomer = State()

class Sorov_state(StatesGroup):
    sorov = State()


class Dars_jadvali_state(StatesGroup):
    guruh_nomi = State()
    filename = State()

class malumot_berish(StatesGroup):
    Jonat = State()