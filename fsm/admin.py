from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

class FSMAdmin(StatesGroup):
    KPI = State()

