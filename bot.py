import config
import logging
import aiogram
import json
import datetime
import re
from aiogram.utils.exceptions import BotBlocked
from aiogram import *

# Инициализация и настройка опроса
dasha = r"https://t.me/dashuluicha"
nameandsurname = {}
sname = str()
# Monday = {}
# Tuesday = {}
# Wednesday = {}
# Thursday = {}
# Friday = {}
# Saturday = {}
# Sunday = {}
# Week = {}
# Mounth = {}
# Дни недели для акций, вводить их будет пользователь с name =  "Менеджер"


# bot init
bot = Bot(token=config.TOKEN)
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
    name = callback.from_user.username
    nameandsurname[userbtn] = username
    await callback.answer(
        f"Охае, чайный мастер {callback.from_user.username} \nЕсли мы уже знакомы - выбери первый пункт \nЕсли нет, то второй!"
        , reply_markup=keyboard)

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
        f"Охае, чайный мастер {callback.from_user.username} \nМы уже знакомы - выбери первый пункт \nЕсли что-то пошло не так, то второй!",
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
                                          callback_data='Центраяльная Чайная История'),
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer("На какой точке ты сегодня работаешь?", reply_markup=keyboard)
    await callback.answer()
    # await bot.send_message(message.from_user.id) берет user id и пишет по нему


# Ответ на второй вопрос
@dp.callback_query_handler(text="3) Я не знаю что делать!")
async def problem1(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Да, нужна помощь', url=dasha),
               types.InlineKeyboardButton(text="Нет, Я запутался в рабочем дне",
                                          callback_data="Нет, Я запутался в рабочем дне")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer("Давай разберемся!\nУ тебя критическая ситуация?", reply_markup=keyboard)
    await callback.answer()
    # await message.answer(reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='Нет, Я запутался в рабочем дне')
async def open_day(callback: types.CallbackQuery):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # buttons = ['Да, нужна помощь', "Нет,Я запутался в рабочем дне"]
    # keyboard.add(*buttons)
    # reply_markup = types.InlineKeyboardButton()
    # Распорядок
    await callback.message.answer('Сообщение 1')
    await callback.message.answer('Сообщение 2')
    await callback.message.answer('Сообщение 3')
    await callback.message.answer('Сообщение 4')


# await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)
# Пушка
@dp.callback_query_handler(text='Чайная История на Пушке')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
               types.InlineKeyboardButton(text="Открыть смену",
                                          callback_data="Открыть смену на пушке"),
               types.InlineKeyboardButton(text='Назад', callback_data='1) Время работать!'),
               types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену на пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await callback.message.answer('Хорошего дня тебе')
    await callback.message.answer(f'Помни, {callback.from_user.username},ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого')
    await callback.message.answer('Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!', reply_markup=keyboard)

@dp.callback_query_handler(text='Распорядок на Пушке')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               # types.InlineKeyboardButton(text="Открыть смену",
               #                            callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Текст распорядка', reply_markup=keyboard)

@dp.callback_query_handler(text='Открыть смену на пушке')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text="Далее",
                                          callback_data="Далее")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Текст открытия смены1')
    await callback.message.answer('Текст открытия смены2')
    await callback.message.answer('Текст открытия смены3')
    await callback.message.answer('Текст открытия смены4', reply_markup=keyboard)

#Тут должна быть продовцовая мудрость
@dp.callback_query_handler(text='Далее')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text="Далее",
                                          callback_data="Далее")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Текст')
    await callback.message.answer('Текст')
    await callback.message.answer('Текст')
    await callback.message.answer('Текст', reply_markup=keyboard)





@dp.callback_query_handler(text='Закрыть смену на пушке')
async def push(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text="Далее",
                                          callback_data="Далее закрытия")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Текст закрытия смены1')
    await callback.message.answer('Текст закрытия смены2')
    await callback.message.answer('Текст закрытия смены3')
    await callback.message.answer('Текст закрытия смены4', reply_markup=keyboard)








# Центральная
@dp.callback_query_handler(text='Центральная Чайная История')
async def central(callback: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text="Открыть смену",
                                          callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await callback.message.answer('Текст открытия смены1')
    await callback.message.answer('Текст открытия смены2')
    await callback.message.answer('Текст открытия смены3')
    await callback.message.answer('Текст открытия смены4', reply_markup=keyboard)

#Тут надо ввести переменную с мудростью




# Хелп с обработкой исключением

@dp.message_handler(text='help')
async def need_help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Бот плохо работает', "/start"]
    keyboard.add(*buttons)
    await message.answer('Что-то не так?', reply_markup=keyboard)
    await message.answer(r"Нажми /start чтобы начать сначала!")


if __name__ == '__main__':
    # executor.start(dp, on_startup())
    executor.start_polling(dp, skip_updates=True)

##################################################################_админская часть_##############################################
# run long-polling
