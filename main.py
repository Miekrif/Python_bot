from loader import dp
import fsm.admin
from aiogram import executor
from utils.functions import open_json
from handlers import message_handlers, callback_query_handlers
from config.config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")


async def on_startup(dp):
    open_json()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
