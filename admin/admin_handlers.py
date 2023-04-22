from loader import dp
from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from admin.admin_states import admin_keyboard, admin_cb

from config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager


# ADMIN_ID = "your_admin_id_here"


# @rate_limit(5, "admin")
@dp.callback_query_handler(text="admin")
async def admin_panel(callback_query: types.CallbackQuery):
    message = callback_query.message
    # Добавьте кнопки на клавиатуру в соответствии с вашими требованиями
    buttons = [types.InlineKeyboardButton("Статистика", callback_data="statistics"),
                types.InlineKeyboardButton("Заблокированные пользователи", callback_data="blocked_users"),
                types.InlineKeyboardButton("Настройки", callback_data="settings")]
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Добавьте кнопки в разметку
    markup.add(*buttons)
    await message.answer("Админская панель", reply_markup=markup)


@dp.callback_query_handler(admin_cb.filter(action=["stats", "users", "close"]))
async def admin_actions(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]

    if action == "stats":
        await query.message.answer("Здесь будет статистика")
    elif action == "users":
        await query.message.answer("Здесь будет управление пользователями")
    elif action == "close":
        await query.message.answer("Админская панель закрыта")
        await query.message.delete_reply_markup()
