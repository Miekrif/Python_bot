from aiogram import types
from loader import dp, bot
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, hbold
from aiogram.dispatcher.filters import Command, Text
from utils.functions import open_json, add_to_dict
from jsons.work_with_jsons import open_json_admins
from config.config import BOT_TOKEN, CHEKICHAT, JSON_FILE, manager


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    id_user = message.from_user.id
    messages = open_json_admins()
    # Проверка является ли пользователь одобренным
    if id_user in messages.get('granted_users', []):
        buttons = [
            types.InlineKeyboardButton(text='1) Время работать !', callback_data='Time_to_work'),
            types.InlineKeyboardButton(text="2) Я не знаю что делать !", callback_data="I_dont_know_what_to_do"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            f"Охае, чайный мастер {message.from_user.first_name} \nМы уже знакомы - выбери первый пункт \nЕсли что-то пошло не так, то второй!",
            reply_markup=keyboard
        )

        # Проверка является ли пользователь админом
        print(id_user)
        print(messages.get('admins', []))
        print(id_user in messages.get('admins', []))
        if id_user in messages.get('admins', []):
            buttons = [types.InlineKeyboardButton(text='Админская панель', callback_data='admin')]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            await message.answer(f"Админская панель", reply_markup=keyboard)

    else:
        buttons = [
            types.InlineKeyboardButton(text='Да, нужна помощь', url=manager),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer(
            f"""Привет, Незнакомец! Для того, чтобы пользоваться мной свяжись с менеджером
            \n Твой id передай его менджеру для добавления тебя в список {id_user}"""
            , reply_markup=keyboard)



@dp.message_handler(commands=['close'])
async def cmd_start(callback: types.Message):
    buttons = [
        types.InlineKeyboardButton(text='Закрыть смену на Пушке', callback_data='Сворачиваемся, ребята'),
        types.InlineKeyboardButton(text='Закрыть смену на Централе', callback_data='Сворачиваемся, ребята'),
        types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной',
                                   callback_data='Сворачиваемся, ребята'),
        types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной',
                                   callback_data='Сворачиваемся, ребята')
    ]
    # first_name = callback.first_name  # Не может быть пустым
    username = callback.from_user.username
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    # for key in nameandsurname.values():
    #
    await callback.answer(
        f"{callback.from_user.first_name}, тебе сейчас надо выбрать точку, на которой ты закрываешь смену!"
        , reply_markup=keyboard)
    await callback.answer()


@dp.message_handler(commands=['open'])
async def cmd_start(callback: types.Message):
    buttons = [types.InlineKeyboardButton(text='Открыть смену', callback_data='Time_to_work')
               ]
    # first_name = callback.first_name  # Не может быть пустым
    username = callback.from_user.username
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    # for key in nameandsurname.values():
    # anig_name(user=)
    await callback.answer(
        f"{callback.from_user.first_name}, Хорошего начала дня!"
        , reply_markup=keyboard)
    await callback.answer()


@dp.message_handler()
async def need_help(message: types.Message):
    if message.chat.type != 'supergroup':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Бот плохо работает', "/start"]
        keyboard.add(*buttons)
        await message.answer(r'Что-то не так?', reply_markup=keyboard)
        await message.answer(r"Нажми /start чтобы начать сначала!")


@dp.message_handler(content_types=["photo"])
async def photo_message(message: types.Message, state: FSMContext):
    global file_id
    file_id = [message.photo[-1].file_id]  # file ID загруженной фотографии
    await state.update_data(file_id=file_id)
    id_user = message.from_user.id
    open_json()
    print(id_user)
    id_user = f'[\'{id_user}\']'
    MY_CONTACT.fromkeys(f'{id_user}')
    if MY_CONTACT.get(id_user) != None:
        global phone1
        print('Не ровняется')
        phone1 = MY_CONTACT.get(id_user)
        phone1 = str(phone1).replace('[', '')
        phone1 = str(phone1).replace(']', '')
        phone1 = str(phone1).replace('"', '')
        phone1 = str(phone1).replace('\'', '')
        messages = [types.InlineKeyboardButton(text="Чайная История на Пушке", callback_data='CHI_on_Pyshka_photo'),
                    types.InlineKeyboardButton(text="Чайная История в парке Революции",
                                               callback_data='CHI_in_Park_Rev_Photo'),
                    types.InlineKeyboardButton(text='Чайная История на Театралке',
                                               callback_data='CHI_on_Teatralka_photo'),
                    types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной',
                                               callback_data='CHI_In_Kras_on_Teatr_photo'),
                    types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной',
                                               callback_data='CHI_In_Kras_on_kras_photo')
                    ]
        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*messages)
        await message.answer(text='Тебя я уже знаю!', reply_markup=keyboard)
    else:
        button_phone = types.KeyboardButton(text="Делись!", request_contact=True)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(button_phone)
        await message.answer(text="Для того, чтобы понять кто прислал чек, мне нужен твой номер", reply_markup=keyboard)

@dp.message_handler(content_types=["contact"])
async def contact_photo(pic2: types.Message, state: FSMContext):
    data = pic2.contact
    phone = str(data)
    phone = re.findall('"phone_number": "[0-9]+"', phone)
    phone = str(phone).replace('"phone_number": "', '+')
    phone = phone.replace('"', '')
    global phone1
    phone1 = phone
    phone1 = str(phone1).replace('[', '')
    phone1 = str(phone1).replace(']', '')
    phone1 = str(phone1).replace('"', '')
    phone1 = str(phone1).replace('\'', '')
    await state.update_data(phone=phone)
    userbtn = str(data)
    userbtn = re.findall('"user_id": [0-9]+', userbtn)
    userbtn = str(userbtn).replace('"user_id": ', '')
    await add_to_dict(userbtn, phone)
    message = [types.InlineKeyboardButton(text="Чайная История на Пушке", callback_data='CHI_on_Pyshka_photo'),
               types.InlineKeyboardButton(text="Чайная История в парке Революции",
                                          callback_data='CHI_in_Park_Rev_Photo'),
               types.InlineKeyboardButton(text='Чайная История на Театралке',
                                          callback_data='CHI_on_Teatralka_photo'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной',
                                          callback_data='CHI_In_Kras_on_Teatr_photo'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной',
                                          callback_data='CHI_In_Kras_on_kras_photo')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*message)
    await bot.send_message(pic2.chat.id, "Выбери свою точку", reply_markup=keyboard)
