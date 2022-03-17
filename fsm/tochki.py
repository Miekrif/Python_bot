# from aiogram import Dispatcher, types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
#
# # Эти значения далее будут подставляться в итоговый текст, отсюда
# # такая на первый взгляд странная форма прилагательных
# available_space = ['Центральная Чайная история(Ростов)', "Центральная История на Пушке(Ростов)", "Чайная история(Краснодар)"]
#
# class OrderFood(StatesGroup):
#     Waiting_photo = State()
#     available_space = State()
#
# async def food_start(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for name in available_space:
#         keyboard.add(name)
#     await message.answer("Выберите точку:", reply_markup=keyboard)
#     await OrderFood.available_space.set()
#
# async def food_chosen(message: types.Message, state: FSMContext):
#     if message.text.lower() not in available_space:
#         await message.answer("Выберите точку из списка ниже:")
#         return
#     await state.update_data(chosen_food=message.text.lower())
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     # Для последовательных шагов можно не указывать название состояния, обходясь next()
#     await OrderFood.next()
#     button_phone = types.KeyboardButton(text="Делись!", request_contact=True)
#     await message.answer("Теперь пожалуйста поделись своим контактом!", reply_markup=keyboard)
#
# async def food_size_chosen(message: types.Message, state: FSMContext):
#     if message.text.lower() not in available_space:
#         await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
#         return
#     user_data = await state.get_data()
#     await message.answer(f"Вы выбрали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
#                          f"Попробуйте теперь заказать напитки: /drinks", reply_markup=types.ReplyKeyboardRemove())
#     await state.finish()