from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
import json
from loader import dp

# Загружаем сообщения
from jsons.work_with_jsons import open_json_admins, read_json_admin_file_add_user, save_json_admins

messages = open_json_admins("messages.json")


# Описываем все состояния
class AdminForm(StatesGroup):
    WaitingForUserAddition = State()
    WaitingForCleaningMessageChange = State()
    WaitingForFile = State()
    WaitingForTradePoint = State()


@dp.callback_query_handler(text='add_user', state=AdminForm.WaitingForUserAddition)
async def admin_add_user(call: types.CallbackQuery):
    await call.message.answer('Пожалуйста, введите ID пользователя, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition)
async def process_add_user(message: types.Message, state: FSMContext):
    user_id = message.text
    read_json_admin_file_add_user(user_id)
    await message.answer('Пользователь успешно добавлен.')
    await state.finish()


# Состояния для FSM
class UpdateCleaningMessageForm(StatesGroup):
    Role = State()
    Message = State()
    Confirm = State()


# Обработчик кнопки "Изменить сообщение об уборке"
@dp.callback_query_handler(text="update_cleaning_message", state="*")
async def cmd_update_cleaning_message(callback: types.CallbackQuery):
    messages = open_json_admins()
    roles_kb = types.InlineKeyboardMarkup(row_width=1)
    for role in messages.get('roles_dict', {}).keys():
        roles_kb.add(types.InlineKeyboardButton(role, callback_data=role))
    await callback.message.edit_reply_markup(reply_markup=roles_kb)
    await UpdateCleaningMessageForm.Role.set()


# Обработчик выбора роли
@dp.callback_query_handler(state=UpdateCleaningMessageForm.Role)
async def process_role(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['role'] = callback.data
    await callback.message.edit_text('Введите новое сообщение об уборке')
    await UpdateCleaningMessageForm.next()


# Обработчик ввода нового сообщения
@dp.message_handler(state=UpdateCleaningMessageForm.Message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
    confirm_kb = types.InlineKeyboardMarkup(row_width=1)
    confirm_kb.add(types.InlineKeyboardButton("Проверить", callback_data="check"))
    confirm_kb.add(types.InlineKeyboardButton("Отменить", callback_data="cancel"))
    confirm_kb.add(types.InlineKeyboardButton("Сохранить", callback_data="save"))
    await message.answer("Новое сообщение: " + message.text, reply_markup=confirm_kb)
    await UpdateCleaningMessageForm.next()


# Обработчик кнопки "Проверить"
@dp.callback_query_handler(text="check", state=UpdateCleaningMessageForm.Confirm)
async def check_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Сообщение проверено и готово к сохранению.')


# Обработчик кнопки "Отменить"
@dp.callback_query_handler(text="cancel", state=UpdateCleaningMessageForm.Confirm)
async def cancel_message(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text('Изменение сообщения отменено')


# Обработчик кнопки "Сохранить"
@dp.callback_query_handler(text="save", state=UpdateCleaningMessageForm.Confirm)
async def save_message(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        messages = open_json_admins()
        messages['roles_dict'][data['role']] = data['message']
        save_json_admins(messages)
    await callback.message.edit_text('Сообщение об уборке успешно обновлено')
    await state.finish()

