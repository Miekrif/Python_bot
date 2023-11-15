from aiogram.utils.callback_data import CallbackData
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command , Text
from aiogram.dispatcher.filters.state import State , StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
import json
from loader import dp , bot
from PDF.logic import start_logic
# Загружаем сообщения
import jsons.work_with_jsons as work_with_jsons

import shutil

messages = work_with_jsons.open_json_admins()


class AddPointForm(StatesGroup):
    WaitingForName = State()
    WaitingForChatID = State()


# Описываем все состояния
class AdminForm(StatesGroup):
    WaitingForUserAddition = State()
    WaitingForUserDell = State()
    WaitingForUserAddition_admin = State()
    WaitingForUserDell_admin = State()
    WaitingForCleaningMessageChange = State()
    WaitingForFile = State()
    WaitingForTradePoint = State()


class DailyCleaningMessage(StatesGroup):
    Role = State()
    Message_show = State()
    Message_edit = State()
    Message_input = State()
    Message = State()
    Confirm = State()


class TradePointRemovalForm(StatesGroup):
    ChoosingPoint = State()


class ScheduleMessageForm(StatesGroup):
    ChoosingPoint = State()
    EditMessage = State()
    NewMessage = State()
    ChooseTime = State()
    DeleteMessage = State()
    SaveChanges = State()
    CancelChanges = State()


@dp.callback_query_handler(text="admin")
async def handle_admin_callback(call: types.CallbackQuery):
    await show_admin_menu(call)
# async def admin_panel(callback: types.CallbackQuery):
#     print(callback.from_user.id , type(callback.from_user.id))
#     if int(callback.from_user.id) in messages.get('admins'):
#         if int(callback.from_user.id) in messages.get('root'):
#             buttons = [
#                 types.InlineKeyboardButton(text='Добавить Нового админа боту' , callback_data='add_admin') ,
#                 types.InlineKeyboardButton(text='Добавить Нового пользователя боту' , callback_data='add_user') ,
#                 types.InlineKeyboardButton(text='Поменять сообщение для уборки' ,
#                                            callback_data='update_cleaning_message') ,
#                 types.InlineKeyboardButton(text='Сделать ценники' , callback_data='get_file') ,
#                 types.InlineKeyboardButton(text='Удалить админа бота' , callback_data='del_admin') ,
#                 types.InlineKeyboardButton(text='Удалить пользователя бота' , callback_data='delete_user') ,
#                 types.InlineKeyboardButton(text='Ежедневное сообщение' , callback_data='schedule_message') ,
#                 types.InlineKeyboardButton(text='Назад' , callback_data='start')
#             ]
#             keyboard = types.InlineKeyboardMarkup(row_width=1)
#             keyboard.add(*buttons)
#         else:
#             buttons = [
#                 types.InlineKeyboardButton(text='Добавить Нового пользователя боту' , callback_data='add_user') ,
#                 types.InlineKeyboardButton(text='Поменять сообщение для уборки' ,
#                                            callback_data='update_cleaning_message') ,
#                 types.InlineKeyboardButton(text='Сделать ценники' , callback_data='get_file') ,
#                 types.InlineKeyboardButton(text='Удалить админа бота' , callback_data='del_admin') ,
#                 types.InlineKeyboardButton(text='Удалить пользователя бота' , callback_data='delete_user') ,
#                 types.InlineKeyboardButton(text='Ежедневное сообщение' , callback_data='schedule_message') ,
#                 types.InlineKeyboardButton(text='Назад' , callback_data='start')
#             ]
#             keyboard = types.InlineKeyboardMarkup(row_width=1)
#             keyboard.add(*buttons)
#         await callback.bot.edit_message_text(
#             chat_id=callback.call.message.chat.id ,  # указываем идентификатор чата
#             message_id=callback.message.message_id ,  # указываем идентификатор сообщения
#             text="Добро пожаловать в админскую панель, выберите функционал:" ,
#             reply_markup=keyboard
#         )


async def show_admin_menu(message_or_call):
    messages = work_with_jsons.open_json_admins()
    if isinstance(message_or_call, types.CallbackQuery):
        chat_id = message_or_call.message.chat.id
    else:
        chat_id = message_or_call.chat.id
    buttons = [
        types.InlineKeyboardButton(text='Добавить Нового пользователя боту' , callback_data='add_user') ,
        types.InlineKeyboardButton(text='Добавить новую точку боту' , callback_data='add_points') ,
        types.InlineKeyboardButton(text='Поменять сообщение для уборки' , callback_data='update_cleaning_message') ,
        types.InlineKeyboardButton(text='Сделать ценники' , callback_data='get_file') ,
        types.InlineKeyboardButton(text='Удалить пользователя бота' , callback_data='delete_user') ,
        types.InlineKeyboardButton(text='Удалить торговую точку из бота' , callback_data='dell_points') ,
        types.InlineKeyboardButton(text='Ежедневное сообщение' , callback_data='schedule_message') ,
    ]
    if int(message_or_call.from_user.id) in messages["users"].get('root'):
        buttons.append(types.InlineKeyboardButton(text='Добавить Нового админа боту' , callback_data='add_admin'))
        buttons.append(types.InlineKeyboardButton(text='Удалить админа бота' , callback_data='del_admin'))
    buttons.append(types.InlineKeyboardButton(text='Назад' , callback_data='start'))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.send_message(chat_id=chat_id , text="Добро пожаловать в админскую панель, выберите функционал:" ,
                           reply_markup=keyboard)


# add an admin
@dp.callback_query_handler(text='add_admin')
async def admin_add_admin(call: types.CallbackQuery):
    await call.message.edit_text('Пожалуйста, введите ID Admin, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition_admin.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition_admin)
async def process_add_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    work_with_jsons.read_json_admin_file_add_user_admin(user_id)
    await bot.send_message(chat_id=message.chat.id , text='Пользователь успешно добавлен.')
    await state.finish()
    await show_admin_menu(message)


# add user
@dp.callback_query_handler(text='add_user')
async def admin_add_user(call: types.CallbackQuery):
    await call.message.edit_text('Пожалуйста, введите ID пользователя, которого хотите добавить:')
    await AdminForm.WaitingForUserAddition.set()


@dp.message_handler(state=AdminForm.WaitingForUserAddition)
async def process_add_user(message: types.Message, state: FSMContext):
    user_id = message.text
    work_with_jsons.read_json_admin_file_add_user(user_id)
    await bot.send_message(chat_id=message.chat.id,
                                text='Пользователь успешно добавлен.')
    await state.finish()
    await show_admin_menu(message)


# Создаем объект CallbackData для обработки данных обратного вызова
delete_user_callback = CallbackData('delete_user' , 'user_id')


#### user deleting
@dp.callback_query_handler(text='delete_user' , state='*')
async def enter_user_delete_state(call: types.CallbackQuery, state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    users = messages["users"]['granted_users']

    keyboard = types.InlineKeyboardMarkup()
    # Создаем кнопку для каждого пользователя
    for user_id in users:
        if str(user_id) == '247548114':
            continue
        button = types.InlineKeyboardButton(
            text=user_id ,
            callback_data=delete_user_callback.new(user_id=user_id) ,
        )
        keyboard.add(button)

    await call.message.edit_text('Выберите пользователя для удаления:' , reply_markup=keyboard)
    await AdminForm.WaitingForUserDell.set()


@dp.callback_query_handler(delete_user_callback.filter() , state=AdminForm.WaitingForUserDell)
async def delete_user(call: types.CallbackQuery, state: FSMContext , callback_data: dict):
    user_id = callback_data['user_id']
    work_with_jsons.del_json_user(user_id)
    await bot.edit_message_text(chat_id=call.message.chat.id , message_id=call.message.message_id ,
                                text=f'Пользователь {user_id} удален.')
    await state.finish()
    await show_admin_menu(call)
###

delete_admin_callback = CallbackData('del_admin' , 'user_id')


##### del admin
@dp.callback_query_handler(text='del_admin' , state='*')
async def enter_user_delete_state(call: types.CallbackQuery, state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    users = messages["users"]['admins']

    keyboard = types.InlineKeyboardMarkup()
    # Создаем кнопку для каждого пользователя
    for user_id in users:
        if str(user_id) == '247548114':
            continue
        button = types.InlineKeyboardButton(
            text=user_id ,
            callback_data=delete_admin_callback.new(user_id=user_id) ,
        )
        keyboard.add(button)

    await call.message.edit_text('Выберите админа для удаления:' , reply_markup=keyboard)
    await AdminForm.WaitingForUserDell_admin.set()


@dp.callback_query_handler(delete_admin_callback.filter() , state=AdminForm.WaitingForUserDell_admin)
async def delete_user(call: types.CallbackQuery, state: FSMContext , callback_data: dict):
    user_id = callback_data['user_id']
    work_with_jsons.del_json_admin(user_id)
    await bot.edit_message_text(chat_id=call.message.chat.id , message_id=call.message.message_id ,
                                text=f'Админ {user_id} удален.')
    await state.finish()
    await show_admin_menu(call)
###


##### message about clearing
# Обработчик кнопки "Изменить сообщение об уборке"
@dp.callback_query_handler(text="update_cleaning_message", state="*")
async def cmd_update_cleaning_message(callback: types.CallbackQuery, state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    roles_kb = types.InlineKeyboardMarkup(row_width=1)
    for role in messages["сlearing"].keys():
        roles_kb.add(types.InlineKeyboardButton(role , callback_data=role))
    await callback.message.edit_reply_markup(reply_markup=roles_kb)
    await DailyCleaningMessage.Role.set()


# Обработчик выбора роли
@dp.callback_query_handler(state=DailyCleaningMessage.Role)
async def process_role(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['point'] = callback.data
    messages = work_with_jsons.open_json_admins()
    roles_kb = types.InlineKeyboardMarkup(row_width=1)
    for role in messages["сlearing"][data['point']].keys():
        roles_kb.add(types.InlineKeyboardButton(role , callback_data=role))

    await callback.message.edit_text('Выберете роль для изменения сообщения:', reply_markup=roles_kb)
    await DailyCleaningMessage.next()


# Вывод старого сообщения
@dp.callback_query_handler(state=DailyCleaningMessage.Message_show)
async def process_edit_message(callback: types.CallbackQuery, state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    async with state.proxy() as data:
        data['role'] = callback.data
    await callback.message.edit_text(f'Текущее сообщение для {data["role"]} в {data["point"]}')
    await callback.message.answer(messages["сlearing"][data['point']][data["role"]])
    await DailyCleaningMessage.Message_edit.set()  # Устанавливаем состояние на Message_edit
    await process_message_edit(callback, state)  # Вызываем функцию обработки process_message_edit


@dp.callback_query_handler(state=DailyCleaningMessage.Message_edit)
async def process_message_edit(callback: types.CallbackQuery, state: FSMContext):
    confirm_kb = types.InlineKeyboardMarkup(row_width=1)
    confirm_kb.add(types.InlineKeyboardButton("Изменить", callback_data="change_daily_message"))
    confirm_kb.add(types.InlineKeyboardButton("Оставить", callback_data="admin"))
    await callback.message.answer("Что с ним сделать?", reply_markup=confirm_kb)
    await DailyCleaningMessage.next()  # Смена состояния происходит уже после того, как пользователь взаимодействует с клавиатурой



@dp.callback_query_handler(text='change_daily_message', state=DailyCleaningMessage.Message_input)
async def process_message_change(callback: types.CallbackQuery):
    await callback.message.answer(text="Введите новое сообщение об уборке:")


# Обработчик ввода нового сообщения
@dp.message_handler(state=DailyCleaningMessage.Message_input)
async def process_message_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
    confirm_kb = types.InlineKeyboardMarkup(row_width=1)
    confirm_kb.add(types.InlineKeyboardButton("Сохранить", callback_data="save"))
    confirm_kb.add(types.InlineKeyboardButton("Изменить", callback_data="change"))
    confirm_kb.add(types.InlineKeyboardButton("Отменить", callback_data="cancel"))
    await message.answer("Что с ним сделать?", reply_markup=confirm_kb)
    await DailyCleaningMessage.Confirm.set()


# Обработчики кнопок "Сохранить", "Изменить", "Отменить"
@dp.callback_query_handler(text="save" , state=DailyCleaningMessage.Confirm)
async def save_message(callback: types.CallbackQuery , state: FSMContext):
    async with state.proxy() as data:
        work_with_jsons.change_message_trade_points(data['point'], data['role'], data['message'])
    await callback.message.edit_text('Сообщение об уборке успешно обновлено')
    await state.finish()
    await show_admin_menu(callback)



@dp.callback_query_handler(text="change", state=DailyCleaningMessage.Confirm)
async def change_message(callback: types.CallbackQuery , state: FSMContext):
    await callback.message.answer("Введите новое сообщение об уборке:")
    await DailyCleaningMessage.Message_input.set()


@dp.callback_query_handler(text="cancel", state=DailyCleaningMessage.Confirm)
async def cancel_message(callback: types.CallbackQuery , state: FSMContext):
    await callback.message.edit_text('Изменение сообщения отменено')
    await state.finish()
    await show_admin_menu(callback)

###

########## counter
@dp.callback_query_handler(text="get_file")
async def enter_file_state(call: types.CallbackQuery, state: FSMContext):
    await bot.send_document(chat_id=call.message.chat.id , document=open('PDF/example.xlsx' , 'rb'))
    buttons = [
        types.InlineKeyboardButton(text='Отмена' , callback_data='cancel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.send_message(chat_id=call.message.chat.id ,
                           text="Я отослал тебе файл, это пример того что я должен получить от тебя для положительного результата \nПожалуйста, загрузите файл или нажмите кнопку 'Отмена'." ,
                           reply_markup=keyboard)
    await AdminForm.WaitingForFile.set()


@dp.callback_query_handler(text='cancel', state='*')
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await show_admin_menu(call)


@dp.message_handler(state=AdminForm.WaitingForFile, content_types=types.ContentTypes.DOCUMENT)
async def get_file(message: types.Message, state: FSMContext):
    file_id_info = await bot.get_file(message.document.file_id)
    await bot.download_file(file_id_info.file_path, 'PDF/counter.xlsx')
    start_logic()  # функция, которую вы хотите выполнить
    shutil.make_archive("PDF/output" , 'zip' , "PDF/output")
    open('PDF/counter.xlsx')
    await bot.send_document(chat_id=message.chat.id, document=open('PDF/output.zip', 'rb'))
    await state.finish()  # Выход из FSM после обработки файла
    await show_admin_menu(message)
#####


#######add trade point
@dp.callback_query_handler(text='add_points', state='*')
async def process_add_point(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.message.chat.id, "Введите название точки:")
    await AddPointForm.WaitingForName.set()


@dp.message_handler(state=AddPointForm.WaitingForName)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(message.chat.id, "Введите ID чата точки если оно у вас есть, если нет - 0:")
    await AddPointForm.WaitingForChatID.set()


@dp.message_handler(state=AddPointForm.WaitingForChatID)
async def process_chat_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = message.text
    await bot.send_message(message.chat.id, "Добавляю точку...")
    # Предположим, что функция add_sell_point принимает аргументы в виде строк
    work_with_jsons.add_sell_point(data['name'], data['chat_id'])
    await bot.send_message(message.chat.id, "Точка добавлена.")
    await state.finish()
    await show_admin_menu(message)


@dp.callback_query_handler(text='dell_points', state='*')
async def process_delete_points_menu(callback_query: types.CallbackQuery, state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    points = messages["trade_points"].keys()  # функция, возвращающая список всех торговых точек
    keyboard = types.InlineKeyboardMarkup()
    # Создаем кнопку для каждого пользователя
    for point_id in points:
        button = types.InlineKeyboardButton(
            text=point_id ,
            callback_data=str(point_id),
        )
        keyboard.add(button)
    await bot.send_message(callback_query.message.chat.id, text='Выберите точку для удаления:', reply_markup=keyboard)
    await TradePointRemovalForm.ChoosingPoint.set()


@dp.callback_query_handler(state=TradePointRemovalForm.ChoosingPoint)
async def process_delete_point(callback_query: types.CallbackQuery, state: FSMContext):
    point = callback_query.data
    work_with_jsons.dell_trade_point(point)  # функция, удаляющая выбранную торговую точку
    await bot.send_message(callback_query.message.chat.id, f"Точка '{point}' удалена.")
    await state.finish()
    await show_admin_menu(callback_query)


# Обработчик кнопки "Ежедневное сообщение"
@dp.callback_query_handler(text='schedule_message')
async def process_schedule_message(callback_query: types.CallbackQuery , state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    trade_points = messages["trade_points"].keys()
    keyboard = types.InlineKeyboardMarkup()

    # Создаем кнопку для каждой точки
    for point in trade_points:
        button = types.InlineKeyboardButton(text=point , callback_data=f'schedule_message_point:{point}')
        keyboard.add(button)

    await bot.send_message(callback_query.message.chat.id , "Выберите точку:" , reply_markup=keyboard)
    await ScheduleMessageForm.ChoosingPoint.set()


# Обработчик выбора точки
@dp.callback_query_handler(state=ScheduleMessageForm.ChoosingPoint)
async def process_schedule_message_point(callback_query: types.CallbackQuery , state: FSMContext):
    point = callback_query.data.split(':')[1]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text='Изменить ежедневное сообщение' ,
                                   callback_data=f'schedule_message_edit:{point}') ,
        types.InlineKeyboardButton(text='Поменять время ежедневного сообщения' ,
                                   callback_data=f'schedule_message_time:{point}') ,
        types.InlineKeyboardButton(text='Удалить ежедневное сообщение' ,
                                   callback_data=f'schedule_message_delete:{point}') ,
        types.InlineKeyboardButton(text='Сохранить изменения' , callback_data='schedule_message_save') ,
        types.InlineKeyboardButton(text='Отменить изменения' , callback_data='schedule_message_cancel') ,
    ]

    keyboard.add(*buttons)

    await bot.send_message(callback_query.message.chat.id , "Выберите действие:" , reply_markup=keyboard)
    async with state.proxy() as data:
        data['point'] = point

    await ScheduleMessageForm.next()


# Обработчик кнопки "Изменить ежедневное сообщение"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('schedule_message_edit') ,
                           state=ScheduleMessageForm.EditMessage)
async def process_schedule_message_edit(callback_query: types.CallbackQuery , state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    point = callback_query.data.split(':')[1]
    message = messages["scheduled_message"].get(point , "")

    await bot.send_message(callback_query.message.chat.id ,
                           f'Текущее сообщение для {point}: {message}\n\nВведите новое сообщение:')
    await ScheduleMessageForm.next()


# Обработчик ввода нового сообщения
@dp.message_handler(state=ScheduleMessageForm.NewMessage)
async def process_new_message(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

    await bot.send_message(message.chat.id , 'Сообщение успешно обновлено')
    await ScheduleMessageForm.previous()


# Обработчик кнопки "Поменять время ежедневного сообщения"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('schedule_message_time') ,
                           state=ScheduleMessageForm.ChooseTime)
async def process_schedule_message_time(callback_query: types.CallbackQuery , state: FSMContext):
    # Код для выбора времени и сохранения его в FSM
    await ScheduleMessageForm.next()


# Обработчик кнопки "Удалить ежедневное сообщение"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('schedule_message_delete') ,
                           state=ScheduleMessageForm.DeleteMessage)
async def process_schedule_message_delete(callback_query: types.CallbackQuery , state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    point = callback_query.data.split(':')[1]
    work_with_jsons.delete_scheduled_message(point)

    await bot.send_message(callback_query.message.chat.id , 'Ежедневное сообщение успешно удалено')
    await show_admin_menu(callback_query)  # Ваша функция show_admin_menu()


# Обработчик кнопки "Сохранить изменения"
@dp.callback_query_handler(text='schedule_message_save' , state=ScheduleMessageForm.SaveChanges)
async def process_schedule_message_save(callback_query: types.CallbackQuery , state: FSMContext):
    async with state.proxy() as data:
        point = data['point']
        message = data.get('message' , '')
        time = data.get('time' , '')

        work_with_jsons.save_scheduled_message(point , time , message)

    await bot.send_message(callback_query.message.chat.id , 'Изменения успешно сохранены')
    await show_admin_menu(callback_query.message.chat.id)  # Ваша функция show_admin_menu()








