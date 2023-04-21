from loader import dp
from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from admin.admin_states import admin_keyboard, admin_cb


ADMIN_ID = "your_admin_id_here"


@dp.message_handler(text="admin", user_id=ADMIN_ID)
async def admin_panel(message: types.Message):
    markup = admin_keyboard()
    await message.answer("Админская панель", reply_markup=markup)


@dp.callback_query_handler(admin_cb.filter(action=["stats", "users", "close"]), user_id=ADMIN_ID)
async def admin_actions(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]

    if action == "stats":
        await query.message.answer("Здесь будет статистика")
    elif action == "users":
        await query.message.answer("Здесь будет управление пользователями")
    elif action == "close":
        await query.message.answer("Админская панель закрыта")
        await query.message.delete_reply_markup()
