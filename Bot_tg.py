import telebot
from telebot import types
import datetime
import re
#Добавляем библиотеки
bot = telebot.TeleBot("5070474559:AAGHUDS0zxIlLFfp77sGqYKvMnFuMpeSyOw", parse_mode = None);
#Инициализация и настройка опроса
name = '';
surname = '';
# Monday = {}
# Tuesday =
# Wednesday =
# Thursday =
# Friday =
# Saturday =
# Sunday =
# Week =
# Mounth =
#Дни недели для акций, вводить их будет пользователь с name =  "Менеджер"
#Вводим переменные
# bot.polling(none_stop=True, interval=0)
# print('Привет')

@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    if message.text == "Привет" or message.text == "привет":
        bot.send_message('Уважаемый чайный мастер '+name+', прошу, выбери точку!')
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")

@bot.message_handler(commands=['/start', '/help'])
def send_welcome(message):
    bot.send_message(message, 'Привет, неизвестный чайный мастер, давай приступим к знакомвству!')
    bot.send_message(message, 'Пришли мне /reg для начала ')
    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
bot.polling(none_stop=True, interval=0)


send_welcome
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');
#Для имени

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surnme);
    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Тебя зовут ' + name + ' ' + surname + '?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

#Для фамилии

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # сюда код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "no":
        start;



send_welcome
# @bot.message_handler(content_types=['text', 'document'])
# def get_text_messages(message):
#     bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     if message.text == "Привет" or message.text == "привет":
#         bot.send_message('Уважаемый чайный мастер '+name+', прошу, выбери точку!')
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")






    # else:
    #     bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
send_welcome