import json
from aiogram import types
from loader import dp , bot
from PDF.logic import start_logic
from aiogram.utils.markdown import hbold
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import jsons.work_with_jsons as work_with_jsons
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


dp.middleware.setup(LoggingMiddleware())


class Form(StatesGroup):
    ReceiptPhoto = State()  # фото чеков
    CleaningPhotoType = State()  # выбор типа фото уборки
    CleaningPhoto = State()
    SinkPhoto = State()  # раковина
    BinPhoto = State()  # урна
    FloorPhoto = State()  # лестница
    SwitchboardPhoto = State()  # рубильники
    FridgePhoto = State()  # холодильник
    ShiftSum = State()  # сумма смены
    TeaCeremony = State()  # кол-во людей на чайной церемонии
    Reason = State()  # причина 0 на чайной церемонии


@dp.message_handler(Command("close"))
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Фотография чеков"))
    markup.add(KeyboardButton("Фото уборки"))
    markup.add(KeyboardButton("Готово"))
    await message.answer("Вот форма по закрытию смены", reply_markup=markup)
    await Form.ReceiptPhoto.set()


@dp.message_handler(lambda message: message.text == "Фотография чеков", state=Form.ReceiptPhoto)
async def receipt_photo(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Отправить фото"))
    markup.add(KeyboardButton("Вернуться"))
    await Form.ReceiptPhoto.set()
    await message.answer("Пожалуйста, отправьте фотографию чеков или выберите другой пункт", reply_markup=markup)


# ... (Обработчики для каждого из пунктов: Фото уборки, Фотография раковины, и т.д.)


@dp.message_handler(lambda message: message.text == "Фото уборки", state="*")
async def cleaning_photo_type(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton("Фотография раковины"))
    markup.add(KeyboardButton("Пустая урна под барной стойкой и в туалете"))
    markup.add(KeyboardButton("Убранная лестница"))
    markup.add(KeyboardButton("Фото рубильников"))
    markup.add(KeyboardButton("Фото работающего холодильника"))
    markup.add(KeyboardButton("Сумма смены"))
    markup.add(KeyboardButton("Кол-во людей записанных на чайную церемонию"))
    await Form.CleaningPhotoType.set()
    await message.answer("Выберите тип фото уборки", reply_markup=markup)

# ... (Оставшиеся обработчики для каждого пункта, включая логику загрузки фотографий, и ввод текста)

# Вы можете продолжить аналогично для каждого из пунктов, создавая кнопки и переходя от одного состояния к другому.
# Продолжение импорта:

from aiogram.types import InputFile


# ...

# Обработка пункта 1 - Фотография чеков:

@dp.message_handler(lambda message: message.text == "Фотография чеков" , state=Form.ReceiptPhoto)
async def ask_receipt_photo(message: types.Message):
    await Form.ReceiptPhoto.set()
    markup = ReplyKeyboardMarkup(resize_keyboard=True , selective=True)
    markup.add(KeyboardButton("Отменить"))
    await message.answer("Пожалуйста, отправьте фотографию чеков." , reply_markup=markup)


@dp.message_handler(content_types=['photo'] , state=Form.ReceiptPhoto)
async def handle_receipt_photo(message: types.Message , state: FSMContext):
    await state.update_data(receipt_photo=message.photo[-1].file_id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True , selective=True)
    markup.add(KeyboardButton("Фотография чеков"))
    markup.add(KeyboardButton("Фото уборки"))
    markup.add(KeyboardButton("Готово"))

    await message.answer("Фотография чеков сохранена. Выберите следующий пункт или завершите отправку данных." ,
                         reply_markup=markup)
    await Form.CleaningPhotoType.set()


@dp.message_handler(lambda message: message.text == "Отменить" , state=Form.ReceiptPhoto)
async def cancel_receipt_photo(message: types.Message , state: FSMContext):
    await state.finish()
    await message.answer("Вы отменили отправку фотографии чеков." , reply_markup=ReplyKeyboardRemove())


# Обработка пункта 2 - Фото уборки:

@dp.message_handler(lambda message: message.text == "Фото уборки" , state=Form.CleaningPhotoType)
async def ask_cleaning_photo_type(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True , selective=True)
    markup.add(KeyboardButton("Фотография раковины"))
    markup.add(KeyboardButton("Пустая урна под баркой и в туалете"))
    markup.add(KeyboardButton("Убранная летка"))
    markup.add(KeyboardButton("Фото рубильников"))
    markup.add(KeyboardButton("Фото работающего холодильника"))
    markup.add(KeyboardButton("Отменить"))

    await Form.CleaningPhoto.set()  # Устанавливаем состояние на ожидание фотографии уборки
    await message.answer("Выберите, какое фото уборки вы хотите отправить:" , reply_markup=markup)


# Далее вы можете создать обработчики для каждого из вариантов фотографий уборки.

@dp.message_handler(lambda message: message.text == "Фотография раковины" , state=Form.CleaningPhoto)
async def ask_sink_photo(message: types.Message):
    await message.answer("Сделайте фото пустой раковины (вся посуда должна быть помыта, и зоны раковины).")


# ... [добавьте обработчики для остальных фотографий уборки по аналогии]


@dp.message_handler(lambda message: message.text == "Отменить" , state=Form.CleaningPhoto)
async def cancel_cleaning_photo(message: types.Message , state: FSMContext):
    await state.finish()
    await message.answer("Вы отменили отправку фотографий уборки." , reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'] , state=Form.CleaningPhoto)
async def handle_cleaning_photo(message: types.Message , state: FSMContext):
    # В данном контексте, мы просто сохраняем фото уборки. В реальном коде вы, возможно, захотите сохранять фотографии отдельно по типам.
    await state.update_data(cleaning_photo=message.photo[-1].file_id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True , selective=True)
    markup.add(KeyboardButton("Фотография чеков"))
    markup.add(KeyboardButton("Фото уборки"))
    markup.add(KeyboardButton("Готово"))

    await message.answer("Фото уборки сохранено. Выберите следующий пункт или завершите отправку данных." ,
                         reply_markup=markup)
    await Form.CleaningPhotoType.set()


# Когда всё будет готово:

@dp.message_handler(lambda message: message.text == "Готово", state="*")
async def finish(message: types.Message, state: FSMContext):
    # Сбор данных и отправка
    await state.finish()
    await message.answer("Данные отправлены!", reply_markup=ReplyKeyboardRemove())




