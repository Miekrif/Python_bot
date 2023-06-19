from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config.config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager

admin_cb = CallbackData("admin", "action")

def admin_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("КПИ", callback_data=admin_cb.new(action="KPI")))
    markup.add(InlineKeyboardButton("уборка", callback_data=admin_cb.new(action="stats")))
    markup.add(InlineKeyboardButton("KPI", callback_data=admin_cb.new(action="stats")))
    markup.add(InlineKeyboardButton("Фин цели на смену", callback_data=admin_cb.new(action="users")))
    markup.add(InlineKeyboardButton("Закрыть админскую панель", callback_data=admin_cb.new(action="close")))
    return markup
