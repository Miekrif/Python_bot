import os
from datetime import *
import logging
import json
from datetime import *
import random
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pathlib import Path
from dotenv import load_dotenv
import re
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cleaning import *
# from cleaning import send_mess
# from cleaning import KPI_lines

storage = MemoryStorage()

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.environ['TOKEN']
# TOKEN = os.environ['TOKEN_test']



# Переменные
# KPI = os.environ['KPI']
chekichat = os.environ['chekichat']
dasha = os.environ['dasha']
nameandsurname = {}
sname = str()
phonenumber = []
tochka_Pushka = 0
tochka_Central = 0
rashod = os.environ['rashod']
user_id = list()
# name = []

def open_json():
    with open('nameandsurname.json') as json_for_dict:
        global MY_CONTACT
        MY_CONTACT = json.load(json_for_dict)
        return MY_CONTACT

async def add_to_dict(userbtn, phone):
    MY_CONTACT[userbtn] = [(phone)]
    with open(r'nameandsurname.json', 'w') as json_for_dict:
        json.dump(MY_CONTACT, json_for_dict)


# # bot init
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# log lvl
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
#################################################################################################################################

async def word_mentor():
    k = 1
    i = 1
    global Words
    Words = []
    while i != 0:
        line = word_book[f'A{k}'].value
        k += 1
        # print(line)
        Words.append(line)
        if line == None:
            i = 0
            Words.pop()
            a_send_message = random.choice(Words)


def anig():
    global user_id
    user_id = list()

class FILE_ID_it(StatesGroup):
    USER_id_input = State()
    Primary_user_id_on_sassion = State()
###########################################################_общая часть_#########################################################


# start message
@dp.message_handler(lambda message: message.text == '/start')
async def cmd_start(message: types.Message):
    id_telo = message.from_user.id
    open_json()
    print(id_telo)
    id_telo = f'[\'{id_telo}\']'
    print(MY_CONTACT)
    MY_CONTACT.fromkeys(f'{id_telo}')
    if MY_CONTACT.get(id_telo) != None:
        buttons = [types.InlineKeyboardButton(text='1) Время работать!', callback_data='1) Время работать!'),
                   types.InlineKeyboardButton(text="2) Я не знаю что делать!",
                                              callback_data="3) Я не знаю что делать!"),
                   ]
        # first_name = callback.first_name  # Не может быть пустым
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            f"Охае, чайный мастер {message.from_user.first_name} \nМы уже знакомы - выбери первый пункт \nЕсли что-то пошло не так, то второй!",
            reply_markup=keyboard)
    else:
        buttons = [types.InlineKeyboardButton(text='1) Время работать!', callback_data='1) Время работать!'),
                   types.InlineKeyboardButton(text='2)Давай знакомиться', callback_data='Знакомвство'),
                   types.InlineKeyboardButton(text="3) Я не знаю что делать!", callback_data="3) Я не знаю что делать!"),
                   ]
        await KPI_lines()
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            f"Охае, чайный мастер {message.from_user.first_name} \nЕсли мы уже знакомы - выбери первый пункт \nЕсли нет, то второй!"
            ,reply_markup=keyboard)

    # return name



@dp.callback_query_handler(text='start')
async def cmd_start(message: types.Message):
    buttons = [types.InlineKeyboardButton(text='1) Время работать!', callback_data='1) Время работать!'),
               types.InlineKeyboardButton(text="2) Я не знаю что делать!", callback_data="3) Я не знаю что делать!"),
               ]
    # first_name = callback.first_name  # Не может быть пустым
    await bot.edit_message_text(text="text")
    username = message.from_user.username
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer(
        f"Охае, чайный мастер {message.from_user.first_name} \nМы уже знакомы - выбери первый пункт \nЕсли что-то пошло не так, то второй!",
        reply_markup=keyboard
    )
    await message.answer()


# Знакомвство
@dp.callback_query_handler(text='Знакомвство')
async def meeting(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Написать ему в телеграмме', url='https://t.me/Itisialready'),
               types.InlineKeyboardButton(text='Следить за ним в инст', url='https://www.instagram.com/chepozrat/'),
               types.InlineKeyboardButton(text='Назад', callback_data='start')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        'Я телеграмм бот написанный для облегчения твоей работы \n Мой создатель @Itisialready aka Влад, связь с ним:',
        reply_markup=keyboard)
    await callback.answer()


# Ответ на первый вопрос
@dp.callback_query_handler(text='1) Время работать!')
async def time_to_work(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Чайная История на Пушке', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text='Центральная Чайная История',callback_data='Центральная чайная история'),
               types.InlineKeyboardButton(text='Чайная История в парке Революции', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной', callback_data='Чайная История в Краснодаре'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной', callback_data='Чайная История в Краснодаре')
               ]
    await word_mentor()
    # print(send_mess.a_send_message)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer("Цитата дня:\n")
    # b = run(random.choice(lines))
    await callback.message.answer(random.choice(Words))
    # await callback.message.answer(b)
    await callback.message.answer("На какой точке ты сегодня работаешь?", reply_markup=keyboard)
    await callback.answer()


    # await bot.send_message(message.from_user.id) берет user id и пишет по нему


# Ответ на второй вопрос
@dp.callback_query_handler(text="3) Я не знаю что делать!")
async def problem1(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Да, нужна помощь', url=dasha),
               types.InlineKeyboardButton(text="Нет, Я запутался в рабочем дне",
                                          callback_data="Нет, Я запутался в рабочем дне")
        , types.InlineKeyboardButton(text='Регламент', callback_data='Регламент'),
               types.InlineKeyboardButton(text='Должностная инструкция', callback_data='Должностная инструкция'),
               types.InlineKeyboardButton(text='Миссия компании', callback_data='Миссия компании'),
               types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer("Давай разберемся!\nУ тебя критическая ситуация?", reply_markup=keyboard)
    await callback.answer()
    # await message.answer(reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='Нет, Я запутался в рабочем дне')
async def open_day(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='3) Я не знаю что делать!')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    # Распорядок
    await callback.message.answer('Сообщение 1')
    await callback.message.answer('Сообщение 2')
    await callback.message.answer('Сообщение 3')
    await callback.message.answer('Сообщение 4', reply_markup=keyboard)
    await callback.answer()


# Пушка
@dp.callback_query_handler(text='Чайная История на Пушке')
async def push(callback: types.CallbackQuery, state: FSMContext):
    day = datetime.now()
    await do_cleaning_pyshk(day)
    a = str(await do_cleaning_pyshk(day)).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену на пушке"),
        types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    # await po_tochkam(tochka='Чайная История на Пушке')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await callback.message.answer(f'Так же не забудь про уборочку! \n\n{await do_cleaning_cchi(day)}')
    a = 0
    print(a)
    await callback.message.answer(f'Хорошего дня тебе,\U0001F609 {callback.from_user.first_name} \n ')
    await callback.message.answer(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await callback.message.answer(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)

#ЦЧИ
@dp.callback_query_handler(text='Центральная чайная история')
async def push(callback: types.CallbackQuery):
    day = datetime.now()
    await do_cleaning_cchi(day)
    a = str(await do_cleaning_cchi(day)).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену на пушке"),
        types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    # await po_tochkam(tochka='Центральная Чайная история')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await callback.message.answer(f'Так же не забудь про уборочку! \n\n{await do_cleaning_cchi(day)}')
    a = 0
    print(a)
    await callback.message.answer(f'Хорошего дня тебе,\U0001F609 {callback.from_user.first_name} ')
    await callback.message.answer(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await callback.message.answer(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)
    await callback.answer()
    # await FILE_ID_it.USER_id_input.set()
    # await state.update_data(id=callback.from_user.id)

#Краснодар
@dp.callback_query_handler(text='Чайная История в Краснодаре')
async def push(callback: types.CallbackQuery, state: FSMContext):
    day = datetime.now()
    await do_cleaning_kchi(day)
    a = str(await do_cleaning_pyshk(day)).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену в Красе"),
        types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    # await po_tochkam(tochka='Чайная История на Пушке')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await callback.message.answer(f'Так же не забудь про уборочку! \n\n{await do_cleaning_kchi(day)}')
    a = 0
    print(a)
    await callback.message.answer(f'Хорошего дня тебе,\U0001F609 {callback.from_user.first_name} \n ')
    await callback.message.answer(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await callback.message.answer(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)



@dp.callback_query_handler(text='Распорядок на Пушке')
async def pushday(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               # types.InlineKeyboardButton(text="Открыть смену",
               #                            callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Текст распорядка', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Открыть смену на пушке')
async def pushopen(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сделал, двигаем дальше",
                                          callback_data="Сделал, двигаем дальше"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(' НУЖНО сделать по порядку\n⬇⬇⬇⬇⬇⬇⬇⬇')
    await callback.message.answer('1 - вынести всё необходимое наулицу')
    await callback.message.answer('2 - проверить мусорные пакеты')
    await callback.message.answer('3 - поставить кипятиться воду', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Сделал, двигаем дальше')
async def gonext(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Все гууд",
                                          callback_data="Все гууд"),
               types.InlineKeyboardButton(text='Есть проблема...', url=dasha),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        '💰💰💰💰💰💰💰💰💰💰💰💰 \nТеперь посчитай остаток денег в кассе и сравни с тем что в таблице.',
        reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Все гууд')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Готово",
                                          callback_data="Готово"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Вода уже наверное вскипела,заливай тэрмоса, заваривай велкомдринк')
    await callback.message.answer('Открывай смену в 1С')
    await callback.message.answer('Проверь телефон на заряд')
    await callback.message.answer('Включи музыку на улице', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Готово')
async def push(callback: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Все чики бамбони",
                                   callback_data="Все чики бамбони"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        'ОСТАЛОСЬ ЧУТЬ ЧУТЬ до ДЗЕНА\n🧶🧶🧶🧶🧶🧶🧶🧶🧶🧶\nПройдиcь по точкам чистоты этого дня:')
    await callback.message.answer(
        '-Протереть столешницу бара.\n-Проверить выкладку товара и ценники.\n-Уборка Санузла\n-Опрыскать цветы\n-Уборка холодильника\n-Вымыть лицо барной стойки',
        reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Все чики бамбони")
async def push(callback: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Старт",
                                   callback_data="Старт"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'{callback.from_user.first_name}\n😇😇😇😇😇')
    await callback.message.answer('БЛАГОДАРИМ ЗА ПОРЯДОК !\nВЕДЬ ТОЛЬКО В ЧИСТОТЕ И ПОРЯДКЕ ВОДИТСЯ ИЗОБИЛИЕ 💰',
                                  reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Старт")
async def closesmena(callback: types.CallbackQuery):
    a = await KPI_lines()
    a = str(a).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
    # a = str(a).replace(']', '')
    # a = str(a).replace(r'\n', '')
    # a = str(a).replace(r"'", '')
    # a = str(a).replace(r" ", '')
    # a = str(a).replace(r",", '\n')
    buttons = [
        types.InlineKeyboardButton(text="Закрыть смену",
                                   callback_data="Закрыть смену"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'{callback.from_user.first_name}')
    # Здесь будет переменная которую будут менять
    await callback.message.answer(
        f'''Твой КПИ на это месяц. \n\n{a}''',
        reply_markup=keyboard)
    await callback.answer()

#KRASNODAR#########################
@dp.callback_query_handler(text='Открыть смену в Красе')
async def pushopen(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сделал, двигаем дальше",
                                          callback_data="Сделал, двигаем дальше Краснодаре"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(' НУЖНО сделать по порядку\n⬇⬇⬇⬇⬇⬇⬇⬇')
    await callback.message.answer('1 - вынести всё необходимое наулицу')
    await callback.message.answer('2 - проверить мусорные пакеты')
    await callback.message.answer('3 - поставить кипятиться воду', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Сделал, двигаем дальше Краснодаре')
async def gonext(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Все гууд",
                                          callback_data="Все гууд в Краснодаре"),
               types.InlineKeyboardButton(text='Есть проблема...', url=dasha),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        '💰💰💰💰💰💰💰💰💰💰💰💰 \nТеперь посчитай остаток денег в кассе и сравни с тем что в таблице.',
        reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Все гууд в Краснодаре')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Готово",
                                          callback_data="Готово в Краснодаре"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Вода уже наверное вскипела,заливай тэрмоса, заваривай велкомдринк')
    await callback.message.answer('Открывай смену в 1С')
    await callback.message.answer('Проверь телефон на заряд')
    await callback.message.answer('Включи музыку на улице', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Готово в Краснодаре')
async def push(callback: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Все чики бамбони",
                                   callback_data="Все чики бамбони в Краснодаре"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        'ОСТАЛОСЬ ЧУТЬ ЧУТЬ до ДЗЕНА\n🧶🧶🧶🧶🧶🧶🧶🧶🧶🧶\nПройдиcь по точкам чистоты этого дня:')
    await callback.message.answer(
        '-Протереть столешницу бара.\n-Проверить выкладку товара и ценники.\n-Уборка Санузла\n-Опрыскать цветы\n-Уборка холодильника\n-Вымыть лицо барной стойки',
        reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Все чики бамбони в Краснодаре")
async def push(callback: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Старт",
                                   callback_data="Старт в Краснодаре"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре ')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'{callback.from_user.first_name}\n😇😇😇😇😇')
    await callback.message.answer('БЛАГОДАРИМ ЗА ПОРЯДОК !\nВЕДЬ ТОЛЬКО В ЧИСТОТЕ И ПОРЯДКЕ ВОДИТСЯ ИЗОБИЛИЕ 💰',
                                  reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Старт в Краснодаре")
async def closesmena(callback: types.CallbackQuery):
    a = await KPI_kras_lines()
    a = str(a).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
    buttons = [
        types.InlineKeyboardButton(text="Закрыть смену",
                                   callback_data="Закрыть смену"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'{callback.from_user.first_name}')
    # Здесь будет переменная которую будут менять
    await callback.message.answer(
        f'''Твой КПИ на это месяц. \n\n{a}''',
        reply_markup=keyboard)
    await callback.answer()


###################################
@dp.callback_query_handler(text='Закрыть смену')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Отлично закрыл\n💰💰😅💰💰",
                                          callback_data="Отлично закрыл"),
               types.InlineKeyboardButton(text="Плохо закрыл\n😔",
                                          callback_data="Плохо закрыл"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'Как прошел день {callback.from_user.first_name} ?', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text='Отлично закрыл')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сворачиваемся, ребята", callback_data="Сворачиваемся, ребята")
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    # await callback.message.answer(f'Как прошел день {callback.from_user.first_name} ?', reply_markup=keyboard)
    await callback.message.answer('Супер !💰 \n Давай теперь вместе закроем смену.\nПОЕХАЛИ !)', reply_markup=keyboard)
    # await callback.message.answer('Текст закрытия смены3')
    # await callback.message.answer('Текст закрытия смены4', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Сворачиваемся, ребята")
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Готово", callback_data="Готово2")
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'ДЕЛАЙ ВСЁ ПО ПОРЯДКУ\n⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇ ')
    await callback.message.answer(
        '- Убрать со столов всю посуду.\n-Вымыть посуду, протереть, поставить на полки.\n-Вымыть чабани, поддоны и поставить на сушку, придвинуть стулья у столов и у бара,сложить пледы.'
        '\n-Навести порядок на баре и на рабочем столе\n-Опустошить термосы от перекипевшей воды.\n-Занести летнюю веранду, стулья, подушки.\n-Вынести мусор.',
        reply_markup=keyboard)
    # await callback.message.answer('Текст закрытия смены3')
    # await callback.message.answer('Текст закрытия смены4', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Готово2")
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="СДЕЛАЛ, гуд бай", callback_data="СДЕЛАЛ, гуд бай"),
               # types.InlineKeyboardButton(text="Напомни, как закрыать смену", url=""),
               # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'ТЕПЕРЬ ЗАЙМЕМСЯ 1С и ТАБЛИЦЕЙ\n⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇ ')
    await callback.message.answer(
        "---  Считаем наличку в кассе, заносим в таблу.\n---  Закрываем смену в 1С,заносим в таблу.\n--- Отправляй фото чеков мне(боту) и я перешлю их менеджеру\n---  Выключаем свет врубильнике.\n---  Закрываем магазин.",
        reply_markup=keyboard)
    # await callback.message.answer('Текст закрытия смены3')
    # await callback.message.answer('Текст закрытия смены4', reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(text="СДЕЛАЛ, гуд бай")
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Отправить чек",
                                          callback_data="Отправить чек")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        f'Ну вот ты и подошел к заключающему фактору нашей встречи сегодня!\nЗаходи ко мне завтра, я ведь буду скучать по тебе!\nПожалуйста не забудь прилать мне фотографию чеков \n\n\nДо скорой встречи',
        reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(text="Отправить чек")
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Отправить чек",
                                          callback_data="Отправить чек")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'Отправляй чек, я ловлю!', reply_markup=keyboard)
    await callback.message.answer_sticker(r'CAACAgIAAxkBAAEEmxhibtEFTZ4688dKcoatIyq04BViPwACWgADrWW8FGIMKfS80fFyJAQ')
    await callback.answer()


@dp.callback_query_handler(text='Плохо закрыл')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сворачиваемся, ребята",
                                          callback_data="Сворачиваемся, ребята"),
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'Сойдет,но у тебя будет возможность стрельнуть завтра.\nТЫ ЛУЧШИЙ! 💪',
                                  reply_markup=keyboard)
    await callback.answer()


# @dp.message_handler(lambda message: message.text == ['close', 'open'])
@dp.message_handler(commands=['close'])
async def cmd_start(callback: types.Message):
    buttons = [
               types.InlineKeyboardButton(text='Закрыть смену на Пушке', callback_data='Сворачиваемся, ребята'),
               types.InlineKeyboardButton(text='Закрыть смену на Централе', callback_data='Сворачиваемся, ребята'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной', callback_data='Сворачиваемся, ребята'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной', callback_data='Сворачиваемся, ребята')
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
    buttons = [types.InlineKeyboardButton(text='Открыть смену', callback_data='1) Время работать!')
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

@dp.callback_query_handler(text='Плохо закрыл')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сворачиваемся, ребята",
                                          callback_data="Сворачиваемся, ребята"),
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'Сойдет,но у тебя будет возможность стрельнуть завтра.\nТЫ ЛУЧШИЙ! 💪',
                                  reply_markup=keyboard)
    await callback.answer()


# Хелп с обработкой исключений
@dp.message_handler()
async def need_help(message: types.Message):
    a = message.chat.type
    if a != 'supergroup':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Бот плохо работает', "/start"]
        keyboard.add(*buttons)
        await message.answer(r'Что-то не так?', reply_markup=keyboard)
        await message.answer(r"Нажми /start чтобы начать сначала!")


@dp.callback_query_handler(text="Регламент")
async def reglament(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Регламент',
                                          url='https://docs.google.com/document/d/1PtKJEh4C5sq3zWwRSU8VQrMh1EkT7jXlqPuY2gW3vcA/edit'),
               types.InlineKeyboardButton(text="Открыть смену",
                                          callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Регламент доступен по одноименной кнопочке', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Должностная инструкция")
async def dolginstr(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
               types.InlineKeyboardButton(text="Должностная инструкция",
                                          url="https://docs.google.com/document/d/1QZ_50FBmrg89zRkTPr0VX2KwdjykzKQxeMnfsOs43Zk/edit")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Должностная инструкция доступна по одноименной кнопочке', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(text="Миссия компании")
async def mission(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
               types.InlineKeyboardButton(text="Открыть смену",
                                          callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(
        'Наша миссия - подобрать чай с заботой  для Вас, вашего настроения и самочувствия, тем самым сделав вас Счастливей!',
        reply_markup=keyboard)
    await callback.answer()


# @dp.message_handler(message='close')

# Напоминание для текучих
async def choose_your_dinner():
    buttons = [types.InlineKeyboardButton(text='Список расходников', callback_data='РАСХОД'),
               # types.InlineKeyboardButton(text="Открыть смену",
               #                            callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    for user in user_id:
        await bot.send_message(chat_id=user, text="Хей🖖 не забудь заказать расходники ", reply_markup=keyboard)
        await bot.send_message(chat_id=user, text=rashod)





async def scheduler():
    aioschedule.every().wednesday("13:00").do(choose_your_dinner)
    aioschedule.every().day("00:00").do(anig)
    # aioschedule.every().day("00:00").do()
    # aioschedule.every().day("00:00").do(c)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup():
    await asyncio.create_task(scheduler())


#Обработка присылаемого фото
#Оброаботка присылаемого сообщения
@dp.message_handler(content_types=["photo"])
async def photo_message(message: types.Message, state: FSMContext):
    global file_id
    file_id = [message.photo[-1].file_id]  # file ID загруженной фотографии
    await state.update_data(file_id=file_id)
    id_telo = message.from_user.id
    open_json()
    print(id_telo)
    id_telo =f'[\'{id_telo}\']'
    MY_CONTACT.fromkeys(f'{id_telo}')
    if MY_CONTACT.get(id_telo) != None:
        global phone1
        print('Не ровняется')
        phone1 = MY_CONTACT.get(id_telo)
        phone1 = str(phone1).replace('[', '')
        phone1 = str(phone1).replace(']', '')
        phone1 = str(phone1).replace('"', '')
        phone1 = str(phone1).replace('\'', '')
        messages = [
            types.InlineKeyboardButton(text="Чайная История на Пушке", callback_data='Чайная История на Пушке фото'),
            types.InlineKeyboardButton(text='Чайная История в Краснодаре', callback_data='Чайная История в Краснодаре фото'),
            types.InlineKeyboardButton(text='Чайная История на Театралке',
                                       callback_data='Чайная История на Театралке фото')]
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
    message = [types.InlineKeyboardButton(text="Чайная История на Пушке", callback_data='Чайная История на Пушке фото'),
               types.InlineKeyboardButton(text="Чайная История в парке Революции", callback_data='Чайная История в парке Революции фото'),
               types.InlineKeyboardButton(text='Чайная История на Театралке',
                                          callback_data='Чайная История на Театралке фото'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной',
                                          callback_data='Чайная История в Краснодаре на Театральной фото'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной', callback_data='Чайная История в Краснодаре на Красной фото'),
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*message)
    await bot.send_message(pic2.chat.id, "Выбери свою точку", reply_markup=keyboard)


@dp.callback_query_handler(text='Чайная История в парке Революции фото')
async def send_long_message_from(callback: types.CallbackQuery):
    await callback.message.answer('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История на #Пушке'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")
    # await message.answer(text='Положил твой чек в карман!')

@dp.callback_query_handler(text='Чайная История на Пушке фото')
async def send_long_message_from(callback: types.CallbackQuery):
    await callback.message.answer('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История на #Пушке'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")
    # await message.answer(text='Положил твой чек в карман!')


@dp.callback_query_handler(text='Чайная История на Театралке фото')
async def send_long_message_from(callback: types.CallbackQuery):
    # keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    await callback.message.answer('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История на #Театралке'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")
    # await message.answer(text='Положил твой чек в карман!')

@dp.callback_query_handler(text='Чайная История в Краснодаре на Театральной фото')
async def send_long_message_from(callback: types.CallbackQuery):
    await callback.message.answer('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История в #Краснодаре'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")

@dp.callback_query_handler(text='Чайная История в Краснодаре на Красной фото')
async def send_long_message_from(callback: types.CallbackQuery):
    await callback.message.answer('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История в #Краснодаре'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")




if __name__ == '__main__':
    anig()
    # executor.start(dp, on_startup())
    open_json()
    on_startup()
    executor.start_polling(dp, skip_updates=True)






##################################################################_админская часть_##############################################

