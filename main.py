import logging
import fsm.admin
from loader import dp
from aiogram import executor
from initial import copy_initial_file
from utils.functions import open_json
from handlers import message_handlers, callback_query_handlers
from config.config import BOT_TOKEN, CHEKICHAT, ADMINS, JSON_FILE, manager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")


if __name__ == '__main__':
    executor.start_polling(dp)
    copy_initial_file()
