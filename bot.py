import os
from datetime import *
import logging
import aiogram
import json
import datetime
import xlrd
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import aioschedule


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.environ['TOKEN']

# excel
##открываем файл
rb = xlrd.open_workbook(r'userid=name.xls')
# выбираем активный лист
sheet = rb.sheet_by_index(0)
lines = []

for i in range(3):
    for j in range(0, 1):
        # Print the cell values with tab space
        lines.append(sheet.cell_value(i, j))

# Переменные
chekichat = os.environ['chekichat']
dasha = os.environ['dasha']
nameandsurname = {}
sname = str()
phonenumber = []
tochka_Pushka = 0
tochka_Central = 0
rashod = os.environ['rashod']

# bot init
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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


###########################################################_общая часть_#########################################################


# start message
@dp.message_handler(lambda message: message.text == '/start')
async def cmd_start(callback: types.Message):
    buttons = [types.InlineKeyboardButton(text='1) Время работать!', callback_data='1) Время работать!'),
               types.InlineKeyboardButton(text='2)Давай знакомиться', callback_data='Знакомвство'),
               types.InlineKeyboardButton(text="3) Я не знаю что делать!", callback_data="3) Я не знаю что делать!"),
               # types.InlineKeyboardButton(text="Я", url='https://t.me/Itisialready')
               ]
    # first_name = callback.first_name  # Не может быть пустым
    username = callback.from_user.username
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    userbtn = callback.from_user.id
    first_name = callback.from_user.first_name
    global name
    name = [callback.from_user.username]
    nameandsurname[userbtn] = [(username, first_name, name)]
    await callback.answer(
        f"Охае, чайный мастер {callback.from_user.first_name} \nЕсли мы уже знакомы - выбери первый пункт \nЕсли нет, то второй!"
        , reply_markup=keyboard)
    await callback.answer()
    # await message.answer()


@dp.callback_query_handler(text='start')
async def cmd_start(callback: types.Message):
    buttons = [types.InlineKeyboardButton(text='1) Время работать!', callback_data='1) Время работать!'),
               # types.InlineKeyboardButton(text='2)Давай знакомиться', callback_data='Знакомвство'),
               types.InlineKeyboardButton(text="2) Я не знаю что делать!", callback_data="3) Я не знаю что делать!"),
               # types.InlineKeyboardButton(text="Я", url='https://t.me/Itisialready')
               ]
    # first_name = callback.first_name  # Не может быть пустым
    username = callback.from_user.username
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    userbtn = callback.from_user.id
    name = callback.from_user.username
    nameandsurname[userbtn] = username
    await callback.message.answer(
        f"Охае, чайный мастер {callback.from_user.first_name} \nМы уже знакомы - выбери первый пункт \nЕсли что-то пошло не так, то второй!",
        reply_markup=keyboard
    )
    await callback.answer()


# Знакомвство
@dp.callback_query_handler(text='Знакомвство')
async def meeting(callback: types.CallbackQuery):
    # sname = types.InlineKeyboardButton(text='Давай знакомиться', callback=)
    buttons = [types.InlineKeyboardButton(text='Написать ему в телеграмме', url='https://t.me/Itisialready'),
               types.InlineKeyboardButton(text='Следить за ним в инст', url='https://www.instagram.com/chepozrat/'),
               types.InlineKeyboardButton(text='Назад', callback_data='start')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await callback.message.answer(
        'Я телеграмм бот написанный для облегчения твоей работы \n Мой создатель @Itisialready aka Влад, связь с ним:',
        reply_markup=keyboard)
    await callback.answer()


# Ответ на первый вопрос
@dp.callback_query_handler(text='1) Время работать!')
async def time_to_work(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Чайная История на Пушке', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text='Центральная Чайная История',
                                          callback_data='Центральная чайная история'),
               ]
    for i in range(3):
        for j in range(0, 1):
            # Print the cell values with tab space
            lines.append(sheet.cell_value(i, j))
        #     print(i + 1, sheet.cell_value(i, j), end='\t')
        # print('')
    # b = run(random.choice(lines))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer("Цитата дня:\n")
    # b = run(random.choice(lines))
    await callback.message.answer(random.choice(lines))
    # await callback.message.answer(b)
    await callback.message.answer("На какой точке ты сегодня работаешь?", reply_markup=keyboard)
    await callback.answer()
    # await bot.send_message(message.from_user.id) берет user id и пишет по нему
    await callback.answer()

# Ответ на второй вопрос
@dp.callback_query_handler(text="3) Я не знаю что делать!")
async def problem1(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Да, нужна помощь', url=dasha),
               types.InlineKeyboardButton(text="Нет, Я запутался в рабочем дне",
                                          callback_data="Нет, Я запутался в рабочем дне"),
               types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!')
        , types.InlineKeyboardButton(text='Регламент', callback_data='Регламент'),
               types.InlineKeyboardButton(text='Должностная инструкция', callback_data='Должностная инструкция'),
               types.InlineKeyboardButton(text='Миссия компании', callback_data='Миссия компании')

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

# await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)
# Пушка
@dp.callback_query_handler(text='Чайная История на Пушке')
async def push(callback: types.CallbackQuery):
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену на пушке"),
        types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    global tochka_Pushka
    tochka_Pushka += 1
    await callback.message.answer(f'Хорошего дня тебе,\U0001F609 {callback.from_user.first_name} ')
    await callback.message.answer(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await callback.message.answer(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)
    await callback.answer()

@dp.callback_query_handler(text='Центральная чайная история')
async def push(callback: types.CallbackQuery):
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену на пушке"),
        types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    global tochka_Central
    tochka_Central += 1
    await callback.message.answer(f'Хорошего дня тебе,\U0001F609 {callback.from_user.first_name} ')
    await callback.message.answer(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await callback.message.answer(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)
    await callback.answer()


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
    # await callback.message.answer('Текст')
    # await callback.message.answer('Текст')
    # await callback.message.answer('Текст', reply_markup=keyboard)
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
    buttons = [
        types.InlineKeyboardButton(text="Закрыть смену",
                                   callback_data="Закрыть смену"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer(f'{callback.from_user.first_name}')
#Здесь будет переменная которую будут менять
    await callback.message.answer(
        'Твой КПИ на это месяц.\nТЫ можешь больше, чемдумаешь!\nМир чай май\nВОРЛД КАП 2018 ШУ ПУЭР\nЮндэ Цяо Му\nгриб Дин Син\nГаба Голд\nШУ ПУэр Волшебство\n\Дегустация габа РУБИ\n\nДоп каждый +200р чайник исин',
        reply_markup=keyboard)
    await callback.answer()

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
    await callback.message.answer("---  Считаем наличку в кассе, заносим в таблу.\n---  Закрываем смену в 1С,заносим в таблу.\n--- Отправляй фото чеков мне(боту) и я перешлю их менеджеру\n---  Выключаем свет врубильнике.\n---  Закрываем магазин.", reply_markup=keyboard)
    # await callback.message.answer('Текст закрытия смены3')
    # await callback.message.answer('Текст закрытия смены4', reply_markup=keyboard)
    await callback.answer()

# @dp.callback_query_handler(text="СДЕЛАЛ, гуд бай")
# async def push(callback: types.CallbackQuery):
#     buttons = [types.InlineKeyboardButton(text="СДЕЛАЛ, гуд бай", callback_data="СДЕЛАЛ, гуд бай"),
#                # types.InlineKeyboardButton(text="Напомни, как закрыать смену", url=""),
#                # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
#                ]
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons)
#     await callback.message.answer(f'ТЕПЕРЬ ЗАЙМЕМСЯ 1С и ТАБЛИЦЕЙ\n⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇ ')
#     await callback.message.answer("---  Считаем наличку в кассе, заносим в таблу.\n---  Закрываем смену в 1С,заносим в таблу.\n--- Отправляй фото чеков\n---  Выключаем свет врубильнике.\n---  Закрываем магазин.", reply_markup=keyboard)
#     # await callback.message.answer('Текст закрытия смены3')
#     # await callback.message.answer('Текст закрытия смены4', reply_markup=keyboard)
#     await callback.answer()

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

# @dp.callback_query_handler(text="Сворачиваемся, ребята")
# async def push(callback: types.CallbackQuery):
#     buttons = [types.InlineKeyboardButton(text="Сворачиваемся, ребята",
#                                           callback_data="Сворачиваемся, ребята"),
#                # types.InlineKeyboardButton(text="😔",
#                #                            callback_data="Плохо закрыл"),
#                types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
#
#                ]
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons)
#     await callback.message.answer(f'Слабо,но у тебя будет возможность стрельнуть завтра.\nТЫ ЛУЧШИЙ! 💪',
#                                   reply_markup=keyboard)


# # Центральная
# @dp.callback_query_handler(text='Центральная Чайная История')
# async def central(callback: types.CallbackQuery):
#     buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
#                types.InlineKeyboardButton(text="Открыть смену",
#                                           callback_data="Открыть смену")
#                ]
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons)
#     await callback.message.answer('Текст открытия смены1')
#     await callback.message.answer('Текст открытия смены2')
#     await callback.message.answer('Текст открытия смены3')
#     await callback.message.answer('Текст открытия смены4', reply_markup=keyboard)
#     await callback.answer()



# @dp.message_handler(lambda message: message.text == ['close', 'open'])
@dp.message_handler(commands= ['close', 'open'])
async def cmd_start(callback: types.Message):
    buttons = [types.InlineKeyboardButton(text='Открыть смену', callback_data='1) Время работать!'),
               types.InlineKeyboardButton(text='Закрыть смену на Пушке', callback_data='Сворачиваемся, ребята'),
               types.InlineKeyboardButton(text='Закрыть смену на Централе', callback_data='Сворачиваемся, ребята')
               # types.InlineKeyboardButton(text="3) Я не знаю что делать!", callback_data="3) Я не знаю что делать!"),
               # types.InlineKeyboardButton(text="Я", url='https://t.me/Itisialready')
               ]
    # first_name = callback.first_name  # Не может быть пустым
    username = callback.from_user.username
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    userbtn = callback.from_user.id
    first_name = callback.from_user.first_name
    name = callback.from_user.username
    nameandsurname[userbtn] = [(username, first_name)]
    await callback.answer(
        f"{callback.from_user.first_name}, тебе сейчас надо выбрать точку, на которой ты закрываешь смену!"
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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Бот плохо работает', "/start"]
    keyboard.add(*buttons)
    await message.answer('Что-то не так?', reply_markup=keyboard)
    await message.answer(r"Нажми /start чтобы начать сначала!")


@dp.callback_query_handler(text="Регламент")
async def reglament(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Регламент', url='https://docs.google.com/document/d/1PtKJEh4C5sq3zWwRSU8VQrMh1EkT7jXlqPuY2gW3vcA/edit'),
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
    await callback.message.answer('Наша миссия - подобрать чай с заботой  для Вас, вашего настроения и самочувствия, тем самым сделав вас Счастливей!', reply_markup=keyboard)
    await callback.answer()

# @dp.message_handler(message='close')

#Напоминание для текучих
@dp.message_handler()
async def choose_your_dinner():
    buttons = [types.InlineKeyboardButton(text='Список расходников', callback_data='РАСХОД'),
               # types.InlineKeyboardButton(text="Открыть смену",
               #                            callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    for user in name:
        await bot.send_message(chat_id = user, text = "Хей🖖 не забудь заказать расходники ", reply_markup = keyboard)
        await bot.send_message(chat_id = user, text = rashod)


async def scheduler():
    aioschedule.every().wednesday("13:00").do(choose_your_dinner)
    aioschedule.every().day("22:00").do(name = [] )
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())

#Обработка присылаемого фото
@dp.message_handler(content_types=["photo"])
# @dp.callback_query_handler(lambda c: c.data == 'art')
async def photo_message(pic):
    file_id = pic.photo[-1].file_id  # file ID загруженной фотографии
    tochka_Pushka = 0
    tochka_Central = 0
    a = datetime.date.today()
    if tochka_Pushka > tochka_Central:
        inf = 'Чек с точки на Пушкинской'
        await bot.send_photo(chat_id=chekichat, photo=file_id)
        await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {pic.from_user.first_name} и это" + inf)
    elif tochka_Central > tochka_Pushka:
        inf = 'Чек с Центарльной точки'
        await bot.send_photo(chat_id=chekichat, photo=file_id)
        await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {pic.from_user.first_name} и это" + inf)
    else:
        await bot.send_photo(chat_id=chekichat, photo=file_id)
        await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {pic.from_user.first_name} и я не смог понять откуда этот чек(")



# if __name__ == '__main__':
#     executor.start_polling(on_startup=on_startup)

if __name__ == '__main__':
    # executor.start(dp, on_startup())
    executor.start_polling(dp, skip_updates=True)




##################################################################_админская часть_##############################################
# run long-polling
# while True:
#     for i in range(3):
#         for j in range(0, 1):
#             # Print the cell values with tab space
#             lines.append(sheet.cell_value(i, j))
# #             #     print(i + 1, sheet.cell_value(i, j), end = '\t')
# #             # print('')
# #     b = random.choice(lines)

def che():
    for i in lines:
        for j in range(0, 1):
            # Print the cell values with tab space
            lines.append(sheet.cell_value(i, j))
            # print(i + 1, sheet.cell_value(i, j), end = '\t')
    print('')

# @dp.message_handler(commands="send")
# async def pars(msg:types.Message):
#     await bot.send_message(dasha, "@" + msg.from_user.username + ": " + msg.text[6:])