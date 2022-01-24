import config
import logging
import aiogram
import datetime
import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# Инициализация и настройка опроса
nameandsurname = []
# surname = []
# user.id = []
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
# log lvl
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

class Orderpeople(StatesGroup): #orderfood
    waiting_for_name = State() #waiting_for_food_name
    waiting_for_surname = State() #waiting_for_food_size

# async def on_startup( ):
#     print('Я родился')
###########################################################_общая часть_#########################################################
# async def cmd_start(message: types.Message):
#     await message.text('Привет, введи /start')

# start message
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['1) Время работать!','2)Давай знакомиться' ,"3) Я не знаю что делать!"]
    # button_1 = types.KeyboardButton(text="1) Время работать!")
    # keyboard.add(button_1)
    # button_2 = "Я не знаю что делать!"
    keyboard.add(*buttons)
    await message.answer("Охае, чайный мастер\nЕсли мы уже знакомы - выбери первый пункт \nЕсли нет, то второй!",reply_markup=keyboard)


# Ответ на первый вопрос
@dp.message_handler(lambda message: message.text == "1) Время работать!")
async def time_to_work(message: types.Message):
    await message.reply("Жду продолжения цепочки")
    # await bot.send_message(message.from_user.id) берет user id и пишет по нему

# Ответ на второй вопрос
@dp.message_handler(lambda message: message.text == "3) Я не знаю что делать!")
async def problem1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Да, нужна помощь', "Нет, Я запутался в рабочем дне"]
    keyboard.add(*buttons)
    await message.answer("Давай разберемся!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)
    # await message.answer(reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'Нет, Я запутался в рабочем дне')
async def open_day(message: types.Message):
   # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   # buttons = ['Да, нужна помощь', "Нет,Я запутался в рабочем дне"]
   # keyboard.add(*buttons)
    reply_markup = types.ReplyKeyboardRemove()
    await message.answer('Сообщение 1')
    await message.answer('Сообщение 2')
    await message.answer('Сообщение 3')
    await message.answer('Сообщение 4')
   # await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)



# @dp.message_handler(lambda message: message.text == "Давай разберемся")
# async def without_puree(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['Да', "Нет,Я запутался в рабочем дне"]
#     keyboard.add(*buttons)
#     await message.answer('У тебя критическая ситуация?', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == '2)Давай знакомиться')
async def get_know(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['C приятного']
    keyboard.add(*buttons)
    await message.answer('Предлагаю тебе начать с приятного, с знакомства', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выбирай с чего начнем!', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text =='С имени')
async def add(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.username not in nameandsurname:
        nameandsurname.append(message.from_user.username)
        # surname.append('0')
        print('Новый Мастер!')
        print(str(name))
    else:
        pass

            # break
    # for i in name:
    #     keyboard.add(name)
    # await message.answer(r"Введите Имя:", reply_markup=keyboard)
    # await Orderpeople.waiting_for_name.set()
# async def start(message):
#     if message.text == '/reg':
#         message.answer(message.from_user.id, "Как тебя зовут?");
#         bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
#     else:
#         bot.send_message(message.from_user.id, 'Напиши /reg');




@dp.message_handler(commands=['/help'])
async def need_help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Бот плохо работает', "/start"]
    keyboard.add(*buttons)
    await message.answer('Что-то не так?', reply_markup=keyboard)
    await  message.answer(r"Нажми /start чтобы начать сначала!")

##################################################################_админская часть_##############################################
# run long-polling
if __name__ == '__main__':
    # executor.start(dp, on_startup())
    executor.start_polling(dp, skip_updates=True)
