from aiogram.utils.callback_data import CallbackData
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
from jsons.work_with_jsons import open_json_admins, read_json_admin_file_add_user, save_json_admins, read_json_admin_file_add_user_admin, del_json_user
import shutil


messages = open_json_admins()


# Описываем все состояния
class AdminForm(StatesGroup):
    WaitingForUserAddition = State()
    WaitingForUserDell = State()
    WaitingForUserAddition_admin = State()
    WaitingForUserDell_admin = State()
    WaitingForCleaningMessageChange = State()
    WaitingForFile = State()
    WaitingForTradePoint = State()
    Role = State()
    Message = State()
    Confirm = State()


@dp.callback_query_handler(text="admin")
async def admin_panel(callback: types.CallbackQuery):
    print(callback.from_user.id, type(callback.from_user.id))
    if int(callback.from_user.id) in messages.get('admins'):
        if int(callback.from_user.id) in messages.get('root'):
            buttons = [
                types.InlineKeyboardButton(text='Добавить Нового админа боту', callback_data='add_admin'),
                types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
                types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
                types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
                types.InlineKeyboardButton(text='Удалить админа бота', callback_data='del_admin'),
                types.InlineKeyboardButton(text='Удалить пользователя бота', callback_data='delete_user'),
                types.InlineKeyboardButton(text='Назад', callback_data='start')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
        else:
            buttons = [
                types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
                types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
                types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
                types.InlineKeyboardButton(text='Удалить админа бота', callback_data='del_admin'),
                types.InlineKeyboardButton(text='Удалить пользователя бота', callback_data='delete_user'),
                types.InlineKeyboardButton(text='Назад', callback_data='start')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id ,  # указываем идентификатор чата
            message_id=callback.message.message_id ,  # указываем идентификатор сообщения
            text="Добро пожаловать в админскую панель, выберите функционал:" ,
            reply_markup=keyboard
        )


async def show_admin_menu(message: types.Message):
    if message.from_user.id in messages.get('root'):
        buttons = [
            types.InlineKeyboardButton(text='Добавить Нового админа боту', callback_data='add_admin'),
            types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
            types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
            types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
            types.InlineKeyboardButton(text='Удалить админа бота', callback_data='del_admin'),
            types.InlineKeyboardButton(text='Удалить пользователя бота', callback_data='delete_user'),
            types.InlineKeyboardButton(text='Назад', callback_data='start')
        ]
    else:
        buttons = [
            types.InlineKeyboardButton(text='Добавить Нового пользователя боту', callback_data='add_user'),
            types.InlineKeyboardButton(text='Поменять сообщение для уборки', callback_data='update_cleaning_message'),
            types.InlineKeyboardButton(text='Сделать ценники', callback_data='get_file'),
            types.InlineKeyboardButton(text='Удалить админа бота', callback_data='del_admin'),
            types.InlineKeyboardButton(text='Удалить пользователя бота', callback_data='delete_user'),
            types.InlineKeyboardButton(text='Назад', callback_data='start')
        ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer(text="Добро пожаловать в админскую панель, выберите функционал:", reply_markup=keyboard)


# add an admin
@dp.callback_query_handler(text='add_admin')
async def admin_add_admin(call: types.CallbackQuery):
    await call.message.edit_text('Пожалуйста, введите ID Admin, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition_admin.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition_admin)
async def process_add_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    read_json_admin_file_add_user_admin(user_id)
    await bot.send_message(chat_id=message.chat.id, text='Пользователь успешно добавлен.')
    await state.finish()
    await show_admin_menu(message)



#add user
@dp.callback_query_handler(text='add_user')
async def admin_add_user(call: types.CallbackQuery):
    await call.message.edit_text('Пожалуйста, введите ID пользователя, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition)
async def process_add_user(message: types.Message, state: FSMContext):
    user_id = message.text
    read_json_admin_file_add_user(user_id)
    await bot.send_message(chat_id=message.chat.id,
                                text='Пользователь успешно добавлен.')
    await state.finish()
    await show_admin_menu(message)


# Создаем объект CallbackData для обработки данных обратного вызова
delete_user_callback = CallbackData('delete_user', 'user_id')


@dp.callback_query_handler(text='delete_user', state='*')
async def enter_user_delete_state(call: types.CallbackQuery, state: FSMContext):
    messages = open_json_admins()
    users = messages['granted_users']

    keyboard = types.InlineKeyboardMarkup()
    # Создаем кнопку для каждого пользователя
    for user_id in users:
        if str(user_id) == '247548114':
            continue
        button = types.InlineKeyboardButton(
            text=user_id,
            callback_data=delete_user_callback.new(user_id=user_id),
        )
        keyboard.add(button)

    await call.message.edit_text('Выберите пользователя для удаления:', reply_markup=keyboard)
    await AdminForm.WaitingForUserDell.set()


@dp.callback_query_handler(delete_user_callback.filter(), state=AdminForm.WaitingForUserDell)
async def delete_user(callback_query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = callback_data['user_id']
    del_json_user(user_id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=f'Пользователь {user_id} удален.')
    await state.finish()
    await show_admin_menu(callback_query.message)


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
    await bot.edit_message_text(chat_id=message.chat.id , message_id=message.message_id,
                                text="Новое сообщение: " + message.text, reply_markup=confirm_kb)
    await AdminForm.next()


# Обработчик кнопки "Проверить"
@dp.callback_query_handler(text="check", state=AdminForm.Confirm)
async def check_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Сообщение проверено и готово к сохранению.')


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
    await bot.send_message(chat_id=call.message.chat.id,
                           text="Пожалуйста, загрузите файл или нажмите кнопку 'Отмена'.",
                           reply_markup=keyboard)
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
    await show_admin_menu(message)
