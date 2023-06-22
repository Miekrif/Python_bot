from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager
from jsons.work_with_jsons import word_mentor
from loader import dp, bot
from utils.functions import open_json, add_to_dict, open_json
from jsons.work_with_jsons import open_json_admins


@dp.callback_query_handler(text='start')
async def cmd_start(call: types.CallbackQuery):
    id_user = call.from_user.id
    messages = open_json_admins()
    # Проверка является ли пользователь одобренным
    if id_user in messages.get('granted_users', []):
        if id_user in messages.get('admins', []):
            buttons = [
                types.InlineKeyboardButton(text='1) Время работать !' , callback_data='Time_to_work'),
                types.InlineKeyboardButton(text="2) Я не знаю что делать !" , callback_data="I_dont_know_what_to_do"),
                types.InlineKeyboardButton(text='Админская панель', callback_data='admin')
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            await call.message.edit_text(f"Админская панель", reply_markup=keyboard)
        else:
            buttons = [
                types.InlineKeyboardButton(text='1) Время работать !', callback_data='Time_to_work'),
                types.InlineKeyboardButton(text="2) Я не знаю что делать !", callback_data="I_dont_know_what_to_do"),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
        await call.message.edit_text(f"Охае, чайный мастер {call.from_user.first_name} \nМы уже знакомы - выбери первый пункт \nЕсли что-то пошло не так, то второй!", reply_markup=keyboard)
        # Проверка является ли пользователь админом
    else:
        buttons = [
            types.InlineKeyboardButton(text='Да, нужна помощь', url=manager),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await call.message.edit_text(
            f"""Привет, Незнакомец! Для того, чтобы пользоваться мной свяжись с менеджером\n
             Твой id передай его менджеру для добавления тебя в список {id_user}""", reply_markup=keyboard)


# Знакомвство
@dp.callback_query_handler(text='intro')
async def meeting(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Написать ему в телеграмме', url='https://t.me/Itisialready'),
               types.InlineKeyboardButton(text='Следить за ним в инст', url='https://www.instagram.com/chepozrat/'),
               types.InlineKeyboardButton(text='Назад', callback_data='start')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        'Я телеграмм бот написанный для облегчения твоей работы \n Мой создатель @Itisialready aka Влад, связь с ним:',
        reply_markup=keyboard)
    await call.answer()


# Ответ на первый вопрос
@dp.callback_query_handler(text='Time_to_work')
async def time_to_work(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Чайная История на Пушке', callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text='Центральная Чайная История',
                                          callback_data='Центральная чайная история'),
               types.InlineKeyboardButton(text='Чайная История в парке Революции',
                                          callback_data='Чайная История на Пушке'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Красной',
                                          callback_data='Чайная История в Краснодаре'),
               types.InlineKeyboardButton(text='Чайная История в Краснодаре на Театральной',
                                          callback_data='Чайная История в Краснодаре')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text("Цитата дня:\n")
    await call.message.edit_text("На какой точке ты сегодня работаешь?", reply_markup=keyboard)
    await call.answer()

    # await bot.send_message(message.from_user.id) берет user id и пишет по нему


# Ответ на второй вопрос
@dp.callback_query_handler(text="I_dont_know_what_to_do")
async def problem1(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Да, нужна помощь', url=manager),
               types.InlineKeyboardButton(text="Нет, Я запутался в рабочем  дне(",
                                          callback_data="Im_confused")
        , types.InlineKeyboardButton(text='Регламент', callback_data='Регламент'),
               types.InlineKeyboardButton(text='Должностная инструкция', callback_data='Должностная инструкция'),
               types.InlineKeyboardButton(text='Миссия компании', callback_data='Миссия компании'),
               types.InlineKeyboardButton(text='Назад', callback_data='Time_to_work')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text("Давай разберемся!\nУ тебя критическая ситуация?", reply_markup=keyboard)
    await call.answer()
    # await message.answer(reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='Im_confused')
async def open_day(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='I_dont_know_what_to_do')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    # Распорядок
    await call.message.edit_text('Сообщение 1')
    await call.message.edit_text('Сообщение 2')
    await call.message.edit_text('Сообщение 3')
    await call.message.edit_text('Сообщение 4', reply_markup=keyboard)
    await call.answer()


# Пушка
@dp.callback_query_handler(text='Чайная История на Пушке')
async def push(call: types.CallbackQuery, state: FSMContext):
    day = datetime.now()
    await do_cleaning_pyshk(day)
    a = str(await do_cleaning_pyshk(day)).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'",
                                                                                                       '').replace(r",",
                                                                                                                   '\n')
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену на пушке"),
        types.InlineKeyboardButton(text='Назад', callback_data='Time_to_work'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    # await po_tochkam(tochka='Чайная История на Пушке')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Так же не забудь про уборочку! \n\n{await do_cleaning_cchi(day)}')
    a = 0
    print(a)
    await call.message.edit_text(f'Хорошего дня тебе,\U0001F609 {call.from_user.first_name} \n ')
    await call.message.edit_text(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await call.message.edit_text(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)


# ЦЧИ
@dp.callback_query_handler(text='Центральная чайная история')
async def push(call: types.CallbackQuery):
    day = datetime.now()
    await do_cleaning_cchi(day)
    a = str(await do_cleaning_cchi(day)).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(
        r",", '\n')
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену на пушке"),
        types.InlineKeyboardButton(text='Назад', callback_data='Time_to_work'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    # await po_tochkam(tochka='Центральная Чайная история')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Так же не забудь про уборочку! \n\n{await do_cleaning_cchi(day)}')
    a = 0
    print(a)
    await call.message.edit_text(f'Хорошего дня тебе,\U0001F609 {call.from_user.first_name} ')
    await call.message.edit_text(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await call.message.edit_text(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)
    await call.answer()
    # await FILE_ID_it.USER_id_input.set()
    # await state.update_data(id=call.from_user.id)


# Краснодар
@dp.callback_query_handler(text='Чайная История в Краснодаре')
async def push(call: types.CallbackQuery, state: FSMContext):
    day = datetime.now()
    await do_cleaning_kchi(day)
    a = str(await do_cleaning_pyshk(day)).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'",
                                                                                                       '').replace(r",",
                                                                                                                   '\n')
    buttons = [
        # types.InlineKeyboardButton(text='Распорядок', callback_data='Распорядок на Пушке'),
        types.InlineKeyboardButton(text="Открыть смену",
                                   callback_data="Открыть смену в Красе"),
        types.InlineKeyboardButton(text='Назад', callback_data='Time_to_work'),
        types.InlineKeyboardButton(text='Закрыть смену', callback_data='Закрыть смену')
    ]
    # await po_tochkam(tochka='Чайная История на Пушке')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Так же не забудь про уборочку! \n\n{await do_cleaning_kchi(day)}')
    a = 0
    print(a)
    await call.message.edit_text(f'Хорошего дня тебе,\U0001F609 {call.from_user.first_name} \n ')
    await call.message.edit_text(
        'Помни,ты самый лучший мастер на планете и у тебя все получится!\nГлавное хотеть этого \n👌 хорошего начала дня\n😇 хороших посетителей\n🙏 хорошего настроения\n😅 хорошего чая\n🤑 хорошей кассы')
    await call.message.edit_text(
        'Готов ли ты сделать план чемпиона?\nЗря засомневался в тебе\nТвоя награда ждет тебя в нашем чайном мире!',
        reply_markup=keyboard)


@dp.callback_query_handler(text='Распорядок на Пушке')
async def pushday(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке'),
               # types.InlineKeyboardButton(text="Открыть смену",
               #                            callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text('Текст распорядка', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Открыть смену на пушке')
async def pushopen(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сделал, двигаем дальше",
                                          callback_data="Сделал, двигаем дальше"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(' НУЖНО сделать по порядку\n⬇⬇⬇⬇⬇⬇⬇⬇')
    await call.message.edit_text('1 - вынести всё необходимое наулицу')
    await call.message.edit_text('2 - проверить мусорные пакеты')
    await call.message.edit_text('3 - поставить кипятиться воду', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Сделал, двигаем дальше')
async def gonext(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Все гууд",
                                          callback_data="Все гууд"),
               types.InlineKeyboardButton(text='Есть проблема...', url=manager),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        '💰💰💰💰💰💰💰💰💰💰💰💰 \nТеперь посчитай остаток денег в кассе и сравни с тем что в таблице.',
        reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Все гууд')
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Готово",
                                          callback_data="Готово"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text('Вода уже наверное вскипела,заливай тэрмоса, заваривай велкомдринк')
    await call.message.edit_text('Открывай смену в 1С')
    await call.message.edit_text('Проверь телефон на заряд')
    await call.message.edit_text('Включи музыку на улице', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Готово')
async def push(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Все чики бамбони",
                                   callback_data="Все чики бамбони"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        'ОСТАЛОСЬ ЧУТЬ ЧУТЬ до ДЗЕНА\n🧶🧶🧶🧶🧶🧶🧶🧶🧶🧶\nПройдиcь по точкам чистоты этого дня:')
    await call.message.edit_text(
        '-Протереть столешницу бара.\n-Проверить выкладку товара и ценники.\n-Уборка Санузла\n-Опрыскать цветы\n-Уборка холодильника\n-Вымыть лицо барной стойки',
        reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Все чики бамбони")
async def push(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Старт",
                                   callback_data="Старт"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'{call.from_user.first_name}\n😇😇😇😇😇')
    await call.message.edit_text('БЛАГОДАРИМ ЗА ПОРЯДОК !\nВЕДЬ ТОЛЬКО В ЧИСТОТЕ И ПОРЯДКЕ ВОДИТСЯ ИЗОБИЛИЕ 💰',
                                  reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Старт")
async def closesmena(call: types.CallbackQuery):
    KPI_it = []
    await KPI_lines(KPI_it)
    buttons = [
        types.InlineKeyboardButton(text="Закрыть смену",
                                   callback_data="Закрыть смену"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'{call.from_user.first_name}')
    # Здесь будет переменная которую будут менять
    await call.message.edit_text(
        f'''Твой КПИ на это месяц. \n\n{print(*KPI_it)}''',
        reply_markup=keyboard)
    await call.answer()


# KRASNODAR#########################
@dp.callback_query_handler(text='Открыть смену в Красе')
async def pushopen(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сделал, двигаем дальше",
                                          callback_data="Сделал, двигаем дальше Краснодаре"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(' НУЖНО сделать по порядку\n⬇⬇⬇⬇⬇⬇⬇⬇')
    await call.message.edit_text('1 - вынести всё необходимое наулицу')
    await call.message.edit_text('2 - проверить мусорные пакеты')
    await call.message.edit_text('3 - поставить кипятиться воду', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Сделал, двигаем дальше Краснодаре')
async def gonext(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Все гууд",
                                          callback_data="Все гууд в Краснодаре"),
               types.InlineKeyboardButton(text='Есть проблема...', url=manager),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        '💰💰💰💰💰💰💰💰💰💰💰💰 \nТеперь посчитай остаток денег в кассе и сравни с тем что в таблице.',
        reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Все гууд в Краснодаре')
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Готово",
                                          callback_data="Готово в Краснодаре"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text('Вода уже наверное вскипела,заливай тэрмоса, заваривай велкомдринк')
    await call.message.edit_text('Открывай смену в 1С')
    await call.message.edit_text('Проверь телефон на заряд')
    await call.message.edit_text('Включи музыку на улице', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Готово в Краснодаре')
async def push(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Все чики бамбони",
                                   callback_data="Все чики бамбони в Краснодаре"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        'ОСТАЛОСЬ ЧУТЬ ЧУТЬ до ДЗЕНА\n🧶🧶🧶🧶🧶🧶🧶🧶🧶🧶\nПройдиcь по точкам чистоты этого дня:')
    await call.message.edit_text(
        '-Протереть столешницу бара.\n-Проверить выкладку товара и ценники.\n-Уборка Санузла\n-Опрыскать цветы\n-Уборка холодильника\n-Вымыть лицо барной стойки',
        reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Все чики бамбони в Краснодаре")
async def push(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Старт",
                                   callback_data="Старт в Краснодаре"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История в Краснодаре ')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'{call.from_user.first_name}\n😇😇😇😇😇')
    await call.message.edit_text('БЛАГОДАРИМ ЗА ПОРЯДОК !\nВЕДЬ ТОЛЬКО В ЧИСТОТЕ И ПОРЯДКЕ ВОДИТСЯ ИЗОБИЛИЕ 💰',
                                  reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Старт в Краснодаре")
async def closesmena(call: types.CallbackQuery):
    a = await KPI_kras_lines()
    a = str(a).replace('[', '').replace(']', '').replace(r'\n', '').replace(r"'", '').replace(r",", '\n')
    buttons = [
        types.InlineKeyboardButton(text="Закрыть смену",
                                   callback_data="Закрыть смену"),
        types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'{call.from_user.first_name}')
    # Здесь будет переменная которую будут менять
    await call.message.edit_text(
        f'''Твой КПИ на это месяц. \n\n{a}''',
        reply_markup=keyboard)
    await call.answer()


###################################
@dp.callback_query_handler(text='Закрыть смену')
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Отлично закрыл\n💰💰😅💰💰",
                                          callback_data="Отлично закрыл"),
               types.InlineKeyboardButton(text="Плохо закрыл\n😔",
                                          callback_data="Плохо закрыл"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Как прошел день {call.from_user.first_name} ?', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Отлично закрыл')
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сворачиваемся,  ребята", callback_data="Closing_smena")
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    # await call.message.edit_text(f'Как прошел день {call.from_user.first_name} ?', reply_markup=keyboard)
    await call.message.edit_text('Супер !💰 \n Давай теперь вместе закроем смену.\nПОЕХАЛИ !)', reply_markup=keyboard)
    # await call.message.edit_text('Текст закрытия смены3')
    # await call.message.edit_text('Текст закрытия смены4', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Closing_smena")
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Готово", callback_data="Готово2")
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'ДЕЛАЙ ВСЁ ПО ПОРЯДКУ\n⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇ ')
    await call.message.edit_text(
        '- Убрать со столов всю посуду.\n-Вымыть посуду, протереть, поставить на полки.\n-Вымыть чабани, поддоны и поставить на сушку, придвинуть стулья у столов и у бара,сложить пледы.'
        '\n-Навести порядок на баре и на рабочем столе\n-Опустошить термосы от перекипевшей воды.\n-Занести летнюю веранду, стулья, подушки.\n-Вынести мусор.',
        reply_markup=keyboard)
    # await call.message.edit_text('Текст закрытия смены3')
    # await call.message.edit_text('Текст закрытия смены4', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Готово2")
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="СДЕЛАЛ, гуд бай", callback_data="СДЕЛАЛ, гуд бай"),
               # types.InlineKeyboardButton(text="Напомни, как закрыать смену", url=""),
               # types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'ТЕПЕРЬ ЗАЙМЕМСЯ 1С и ТАБЛИЦЕЙ\n⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇ ')
    await call.message.edit_text(
        "---  Считаем наличку в кассе, заносим в таблу.\n---  Закрываем смену в 1С,заносим в таблу.\n--- Отправляй фото чеков мне(боту) и я перешлю их менеджеру\n---  Выключаем свет врубильнике.\n---  Закрываем магазин.",
        reply_markup=keyboard)
    # await call.message.edit_text('Текст закрытия смены3')
    # await call.message.edit_text('Текст закрытия смены4', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="СДЕЛАЛ, гуд бай")
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Отправить чек",
                                          callback_data="Отправить чек")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        f'Ну вот ты и подошел к заключающему фактору нашей встречи сегодня!\nЗаходи ко мне завтра, я ведь буду скучать по тебе!\nПожалуйста не забудь прилать мне фотографию чеков \n\n\nДо скорой встречи',
        reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Отправить чек")
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Отправить чек",
                                          callback_data="Отправить чек")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Отправляй чек, я ловлю!', reply_markup=keyboard)
    await call.message.edit_text_sticker(r'CAACAgIAAxkBAAEEmxhibtEFTZ4688dKcoatIyq04BViPwACWgADrWW8FGIMKfS80fFyJAQ')
    await call.answer()


@dp.callback_query_handler(text='Плохо закрыл')
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сворачиваемся,  ребята",
                                          callback_data="Closing_smena"),
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Сойдет,но у тебя будет возможность стрельнуть завтра.\nТЫ ЛУЧШИЙ! 💪',
                                  reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='Плохо закрыл')
async def push(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text="Сворачиваемся,  ребята",
                                          callback_data="Closing_smena"),
               # types.InlineKeyboardButton(text="😔",
               #                            callback_data="Плохо закрыл"),
               types.InlineKeyboardButton(text='Назад', callback_data='Чайная История на Пушке')

               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f'Сойдет,но у тебя будет возможность стрельнуть завтра.\nТЫ ЛУЧШИЙ! 💪',
                                  reply_markup=keyboard)
    await call.answer()

@dp.callback_query_handler(text="Регламент")
async def reglament(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Регламент',
                                          url='https://docs.google.com/document/d/1PtKJEh4C5sq3zWwRSU8VQrMh1EkT7jXlqPuY2gW3vcA/edit'),
               types.InlineKeyboardButton(text="Открыть смену",
                                          callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text('Регламент доступен по одноименной кнопочке', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Должностная инструкция")
async def dolginstr(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Time_to_work'),
               types.InlineKeyboardButton(text="Должностная инструкция",
                                          url="https://docs.google.com/document/d/1QZ_50FBmrg89zRkTPr0VX2KwdjykzKQxeMnfsOs43Zk/edit")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text('Должностная инструкция доступна по одноименной кнопочке', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text="Миссия компании")
async def mission(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(text='Назад', callback_data='Time_to_work'),
               types.InlineKeyboardButton(text="Открыть смену",
                                          callback_data="Открыть смену")
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(
        'Наша миссия - подобрать чай с заботой  для Вас, вашего настроения и самочувствия, тем самым сделав вас Счастливей!',
        reply_markup=keyboard)
    await call.answer()




@dp.callback_query_handler(text='CHI_in_Park_Rev_Photo')
async def send_long_message_from(call: types.CallbackQuery):
    await call.message.edit_text('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История на #парке_Революции'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")
    # await message.answer(text='Положил твой чек в карман!')


@dp.callback_query_handler(text='CHI_on_Pyshka_photo')
async def send_long_message_from(call: types.CallbackQuery):
    await call.message.edit_text('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История на #Пушке'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")
    # await message.answer(text='Положил твой чек в карман!')


@dp.callback_query_handler(text='CHI_on_Teatralka_photo')
async def send_long_message_from(call: types.CallbackQuery):
    # keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    await call.message.edit_text('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История на #Театралке'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")
    # await message.answer(text='Положил твой чек в карман!')


@dp.callback_query_handler(text='CHI_In_Kras_on_Teatr_photo')
async def send_long_message_from(call: types.CallbackQuery):
    await call.message.edit_text('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История в #Краснодаре_на_Театральной'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")


@dp.callback_query_handler(text='CHI_In_Kras_on_kras_photo')
async def send_long_message_from(call: types.CallbackQuery):
    await call.message.edit_text('Положил твой чек в карман!', reply_markup=None)
    a = date.today()
    # await file_id[0].download(f'cheki/send-{file_id[0].file_unique_id}.jpg')  # Сохраниение чеков
    inf = 'Чайная История в Краснодаре на #Красной'
    await bot.send_photo(chat_id=chekichat, photo=file_id[0])
    file_id.clear()
    await bot.send_message(chat_id=chekichat, text=f"Хей🖖,сегодня {a}, отправил его {phone1} и это {inf}")