from aiogram.dispatcher.filters import Command , Text
from loader import dp , bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
import jsons.work_with_jsons as work_with_jsons
import logging
import handlers.message_handlers as message_handlers


class IntroductionForm(StatesGroup):
    WaitingForName = State()
    WaitingForSurname = State()
    WaitingForNumber = State()


class ChangeDataUsers(StatesGroup):
    ChangeForName = State()
    ChangeForSurname = State()
    ChangeForNumber = State()


@dp.message_handler(state=IntroductionForm.WaitingForName)
async def process_name(message: types.Message, state: FSMContext):
    logging.info('Function process_name is called')
    name = message.text
    if len(name) < 2:
        await bot.send_message(chat_id=message.chat.id,
                               text='Ваше имя должно быть длиннее. Пожалуйста, введите снова:')
    else:
        async with state.proxy() as data:
            data['Name'] = name
        await bot.send_message(chat_id=message.chat.id,
                               text='Теперь введите вашу фамилию')
        await IntroductionForm.next()


@dp.message_handler(state=IntroductionForm.WaitingForSurname)
async def process_surname(message: types.Message, state: FSMContext):
    logging.info('Function process_surname is called')
    surname = message.text
    if len(surname) < 2:
        await bot.send_message(chat_id=message.chat.id,
                               text='Ваша фамилия должна быть длиннее. Пожалуйста, введите снова:')
    else:
        async with state.proxy() as data:
            data['Surname'] = surname
        await bot.send_message(chat_id=message.chat.id,
                               text='Теперь введите ваш номер телефона:')
        await IntroductionForm.next()


@dp.message_handler(state=IntroductionForm.WaitingForNumber)
async def process_phone_number(message: types.Message, state: FSMContext):
    logging.info('Function process_phone_number is called')  # добавлено для логирования
    phone_number = message.text
    if len(phone_number) != 12 or not phone_number.startswith('+7'):
        await bot.send_message(chat_id=message.chat.id, text='Ваш номер телефона должен начинаться с +7 и быть длиной 12 символов. Пожалуйста, введите снова:')
    else:
        async with state.proxy() as data:
            data['phone_number'] = phone_number
        await bot.send_message(chat_id=message.chat.id,
                               text='Теперь сверим данные:')
        logging.info('Going to next state from process_phone_number')  # добавлено для логирования
        async with state.proxy() as data:
            buttons = [
                types.InlineKeyboardButton(text='Изменить', callback_data='change'),
                types.InlineKeyboardButton(text='Готово', callback_data='change_done'),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2).add(*buttons)
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Имя: {data['Name']}\nФамилия: {data['Surname']}\nНомер: {data['phone_number']}\n\nЕсли все данные верны, нажмите 'Готово'. Если вы хотите что-то изменить, нажмите 'Изменить'.",
                                   reply_markup=keyboard)


@dp.callback_query_handler(text='change', state='*')
async def process_change(query, state: FSMContext):
    buttons = [
        types.InlineKeyboardButton(text='Изменить имя' , callback_data='change_name') ,
        types.InlineKeyboardButton(text='Изменить фамилию' , callback_data='change_surname') ,
        types.InlineKeyboardButton(text='Изменить номер' , callback_data='change_phone_number') ,
        types.InlineKeyboardButton(text='Готово' , callback_data='change_done') ,
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)

    # Здесь мы проверяем тип запроса и отправляем соответствующее сообщение
    if isinstance(query , types.Message):
        await bot.send_message(query.chat.id , "Выберите, какие данные вы хотите изменить:" , reply_markup=keyboard)
    elif isinstance(query , types.CallbackQuery):
        await bot.send_message(query.message.chat.id , "Выберите, какие данные вы хотите изменить:" ,
                               reply_markup=keyboard)
    else:
        logging.error(f"Unexpected query type: {type(query)}")


@dp.callback_query_handler(text='change_name', state='*')
async def start_change_name(callback_query: types.CallbackQuery, state: FSMContext):
    await ChangeDataUsers.ChangeForName.set()
    await bot.send_message(callback_query.message.chat.id, "Введите новое имя:")


@dp.message_handler(state=ChangeDataUsers.ChangeForName)
async def process_change_name(message: types.Message, state: FSMContext):
    name = message.text
    if len(name) < 2:
        await bot.send_message(message.chat.id, "Имя должно быть длиннее. Пожалуйста, введите снова:")
    else:
        await state.update_data(Name=name)
        await bot.send_message(message.chat.id, "Имя изменено.")
        await process_change(message, state)


@dp.callback_query_handler(text='change_surname', state='*')
async def start_change_surname(callback_query: types.CallbackQuery, state: FSMContext):
    await ChangeDataUsers.ChangeForSurname.set()
    await bot.send_message(callback_query.message.chat.id, "Введите новую фамилию:")


@dp.message_handler(state=ChangeDataUsers.ChangeForSurname)
async def process_change_surname(message: types.Message, state: FSMContext):
    surname = message.text
    if len(surname) < 2:
        await bot.send_message(message.chat.id, "Фамилия должна быть длиннее. Пожалуйста, введите снова:")
    else:
        await state.update_data(Surname=surname)
        await bot.send_message(message.chat.id, "Фамилия изменена.")
        await process_change(message, state)


@dp.callback_query_handler(text='change_phone_number', state='*')
async def start_change_phone_number(callback_query: types.CallbackQuery, state: FSMContext):
    await ChangeDataUsers.ChangeForNumber.set()
    await bot.send_message(callback_query.message.chat.id, "Введите новый номер телефона:")


@dp.message_handler(state=ChangeDataUsers.ChangeForNumber)
async def process_change_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if len(phone_number) != 12 or not phone_number.startswith('+7'):
        await bot.send_message(message.chat.id, "Ваш номер телефона должен начинаться с +7 и быть длиной 12 символов. Пожалуйста, введите снова:")
    else:
        await state.update_data(phone_number=phone_number)
        await bot.send_message(message.chat.id, "Номер телефона изменен.")
        await process_change(message, state)


@dp.callback_query_handler(text='change_done', state='*')
async def process_change_done(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        work_with_jsons.add_granted_users_is_data(
            callback_query.from_user.id, data['Name'], data['Surname'], data['phone_number'])
        await bot.send_message(callback_query.message.chat.id, "Спасибо! Ваши данные обновлены.")
        await state.finish()
        await message_handlers.cmd_start(callback_query)