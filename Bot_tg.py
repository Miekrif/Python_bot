import telebot
import datetime
import re
#Добавляем библиотеки
bot = telebot.TeleBot('Токен');
bot.polling(none_stop=True, interval=0)
#Инициализация и настройка опроса
name = '';
surname = '';
#Вводим переменные
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
#Для фамилии



@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    if message.text == "Привет" or message.text == "привет":
        bot.send_message('Уважаемый чайный мастер, прошу, выбери точку!')
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")







    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")