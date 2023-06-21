from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
import json
from loader import dp, bot
from PDF.logic import start_logic
# Загружаем сообщения
from jsons.work_with_jsons import open_json_admins, read_json_admin_file_add_user, save_json_admins, read_json_admin_file_add_user_admin
import shutil


messages = open_json_admins()


# Описываем все состояния
class AdminForm(StatesGroup):
    WaitingForUserAddition = State()
    WaitingForUserAddition_admin = State()
    WaitingForCleaningMessageChange = State()
    WaitingForFile = State()
    WaitingForTradePoint = State()
    Role = State()
    Message = State()
    Confirm = State()


@dp.callback_query_handler(text="admin")
async def admin_panel(callback: types.CallbackQuery):
    if callback.from_user.id in messages.get('root'):
        buttons = [
            types.InlineKeyboardButton(text='Добавить Нового админа боту', callback_data='add_admin'),
            types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
            types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
            types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
            types.InlineKeyboardButton(text='Назад', callback_data='start')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
    else:
        buttons = [
            types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
            types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
            types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
            types.InlineKeyboardButton(text='Назад', callback_data='start')
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
    await callback.message.answer("Добро пожаловать в админскую панель, выберите функционал:", reply_markup=keyboard)
    await callback.answer()


async def show_admin_menu(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
        types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
        types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
        types.InlineKeyboardButton(text='Назад', callback_data='start')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Добро пожаловать в админскую панель, выберите функционал:", reply_markup=keyboard)

#add admin
@dp.callback_query_handler(text='add_admin')
async def admin_add_admin(call: types.CallbackQuery):
    await call.message.answer('Пожалуйста, введите ID пользователя, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition_admin.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition_admin)
async def process_add_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    read_json_admin_file_add_user_admin(user_id)
    await message.answer('Пользователь успешно добавлен.')
    await state.finish()
    await show_admin_menu(message)


#add user
@dp.callback_query_handler(text='add_user')
async def admin_add_user(call: types.CallbackQuery):
    await call.message.answer('Пожалуйста, введите ID пользователя, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition)
async def process_add_user(message: types.Message, state: FSMContext):
    user_id = message.text
    read_json_admin_file_add_user(user_id)
    await message.answer('Пользователь успешно добавлен.')
    await state.finish()
    await show_admin_menu(message)


# Обработчик кнопки "Изменить сообщение об уборке"
@dp.callback_query_handler(text="update_cleaning_message", state="*")
async def cmd_update_cleaning_message(callback: types.CallbackQuery):
    messages = open_json_admins()
    roles_kb = types.InlineKeyboardMarkup(row_width=1)
    for role in messages.get('roles_dict', {}).keys():
        roles_kb.add(types.InlineKeyboardButton(role, callback_data=role))
    await callback.message.edit_reply_markup(reply_markup=roles_kb)
    await AdminForm.Role.set()


# Обработчик выбора роли
@dp.callback_query_handler(state=AdminForm.Role)
async def process_role(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['role'] = callback.data
    await callback.message.edit_text('Введите новое сообщение об уборке')
    await AdminForm.next()


# Обработчик ввода нового сообщения
@dp.message_handler(state=AdminForm.Message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
    confirm_kb = types.InlineKeyboardMarkup(row_width=1)
    confirm_kb.add(types.InlineKeyboardButton("Проверить", callback_data="check"))
    confirm_kb.add(types.InlineKeyboardButton("Отменить", callback_data="cancel"))
    confirm_kb.add(types.InlineKeyboardButton("Сохранить", callback_data="save"))
    await message.answer("Новое сообщение: " + message.text, reply_markup=confirm_kb)
    await AdminForm.next()


# Обработчик кнопки "Проверить"
@dp.callback_query_handler(text="check", state=AdminForm.Confirm)
async def check_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Сообщение проверено и готово к сохранению.')


# Обработчик кнопки "Отменить"
@dp.callback_query_handler(text="cancel", state=AdminForm.Confirm)
async def cancel_message(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text('Изменение сообщения отменено')


# Обработчик кнопки "Сохранить"
@dp.callback_query_handler(text="save", state=AdminForm.Confirm)
async def save_message(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        messages = open_json_admins()
        messages['roles_dict'][data['role']] = data['message']
        save_json_admins(messages)
    await callback.message.edit_text('Сообщение об уборке успешно обновлено')
    await state.finish()


@dp.callback_query_handler(text="get_file")
async def enter_file_state(call: types.CallbackQuery, state: FSMContext):
    await bot.send_document(chat_id=call.message.chat.id, document=open('PDF/example.xlsx', 'rb'))
    buttons = [
        types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.answer("Пожалуйста, загрузите файл или нажмите кнопку 'Отмена'.", reply_markup=keyboard)
    await AdminForm.WaitingForFile.set()


@dp.callback_query_handler(text='cancel', state='*')
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await show_admin_menu(call.message)


@dp.message_handler(state=AdminForm.WaitingForFile, content_types=types.ContentTypes.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    file_id_info = await bot.get_file(message.document.file_id)
    await bot.download_file(file_id_info.file_path, 'PDF/counter.xlsx')
    start_logic()  # функция, которую вы хотите выполнить
    open('PDF/counter.xlsx')
    shutil.make_archive("PDF/output", 'zip', "PDF/output")
    await bot.send_document(chat_id=message.chat.id, document=open('PDF/output.zip', 'rb'))

    await state.finish()  # Выход из FSM после обработки файла
