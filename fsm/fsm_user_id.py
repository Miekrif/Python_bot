from aiogram.dispatcher.filters import Command , Text
from loader import dp , bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
import jsons.work_with_jsons as work_with_jsons


class IntroductionForm(StatesGroup):
    WaitingForName = State()
    WaitingForSurname = State()
    WaitingForNumber = State()


@dp.message_handler(Command("start") , state=None)
async def handle_start_command(message: types.Message , state: FSMContext):
    messages = work_with_jsons.open_json_admins()
    id_user = message.from_user.id
    granted_users_info = messages.get('granted_users_is' , {}).get(id_user , {})

    if not granted_users_info or not all(
            field in granted_users_info for field in ['name' , 'surname' , 'phone_number']):
        await IntroductionForm.WaitingForName.set()
        await bot.send_message(chat_id=message.chat.id , text='Пожалуйста, введите ваше имя')


@dp.message_handler(state=IntroductionForm.WaitingForName)
async def process_name(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await IntroductionForm.next()
    await bot.send_message(chat_id=message.chat.id , text='Пожалуйста, введите вашу фамилию')


@dp.message_handler(state=IntroductionForm.WaitingForSurname)
async def process_surname(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await IntroductionForm.next()
    await bot.send_message(chat_id=message.chat.id , text='Пожалуйста, введите ваш номер телефона')


@dp.message_handler(state=IntroductionForm.WaitingForNumber)
async def process_number(message: types.Message , state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    user_introducing(message.from_user.id , data['name'] , data['surname'] , data['phone_number'])
    await state.finish()
    await bot.send_message(chat_id=message.chat.id , text='Спасибо! Ваши данные успешно записаны.')
