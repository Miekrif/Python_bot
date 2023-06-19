from loader import dp
import fsm.admin
from aiogram import executor
from utils.functions import open_json
from handlers import message_handlers, callback_query_handlers
from config.config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager


async def on_startup(dp):
    open_json()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
