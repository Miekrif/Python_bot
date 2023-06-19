from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from loader import dp

# Загружаем сообщения
from jsons.work_with_jsons import open_json_admins

messages = open_json_admins("messages.json")

# Описываем все состояния
class CleaningForm(StatesGroup):
    role = State()
    trade_point = State() # новое состояние
    cleaning = State()
    report = State()
    # add more states if needed

# Команда старта для админов


# Выбор роли
@dp.message_handler(state=CleaningForm.role)
async def process_role(message: types.Message, state: FSMContext):
    # Сохраняем роль
    async with state.proxy() as messages:
        messages['role'] = message.text
    await message.answer(messages["trade_point"], reply_markup=types.ReplyKeyboardRemove())
    await CleaningForm.trade_point.set()

# Выбор торговой точки
@dp.message_handler(state=CleaningForm.trade_point)
async def process_trade_point(message: types.Message, state: FSMContext):
    async with state.proxy() as messages:
        messages['trade_point'] = message.text
    await message.answer(messages["start_cleaning"])
    await CleaningForm.cleaning.set()

# И так далее...
