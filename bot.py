import config
import logging
import aiogram
import datetime
import re
from aiogram import Bot, Dispatcher, executor, types

# Инициализация и настройка опроса
name = '';
surname = '';
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
alert = InlineKeyboardMarkup('https://t.me/studyboiibot', url='https://t.me/studyboiibot')
# log lvl
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


# async def cmd_start(message: types.Message):
#     await message.text('Привет, введи /start')

# start message
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['1) Время работать!', "2) Я не знаю что делать!"]
    # button_1 = types.KeyboardButton(text="1) Время работать!")
    # keyboard.add(button_1)
    # button_2 = "Я не знаю что делать!"
    keyboard.add(*buttons)
    await message.answer("Охае, чайный мастер\nЕсли мы уже знакомы - выбери первый пункт \nЕсли нет, то второй!",
                         reply_markup=keyboard)


# Ответ на первый вопрос
@dp.message_handler(lambda message: message.text == "1) Время работать!")
async def without_puree(message: types.Message):
    await message.reply("Жди продолжения цепочки")


# Ответ на второй вопрос
@dp.message_handler(lambda message: message.text == "2) Я не знаю что делать!")
async def without_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Да, нужна помощь', "Нет,Я запутался в рабочем дне"]
    keyboard.add(*buttons)
    await message.answer("Давай разберемся!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)

#@dp.message_handler(lambda message: message.text == 'Да, нужна помощь')
#async def without_puree(message: types.Message):
#    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#    # buttons = ['Да, нужна помощь', "Нет,Я запутался в рабочем дне"]
#    # keyboard.add(*buttons)
#    # await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)


# @dp.message_handler(lambda message: message.text == "Давай разберемся")
# async def without_puree(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['Да', "Нет,Я запутался в рабочем дне"]
#     keyboard.add(*buttons)
#     await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)

# @dp.message_handler(commands=['help'])
# # async  def send_answer(message: types.Message):
# async def without_puree(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['Да', "Нет,Я запутался в рабочем дне"]
#     keyboard.add(*buttons)
#     await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)
#
#     await  message.answer("У тебя что-то случилось?")


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)

# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
