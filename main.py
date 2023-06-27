import logging
from loader import dp
from aiogram import executor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Информационное сообщение")
logger.warning("Предупреждение")
logger.error("Ошибка")


if __name__ == '__main__':
    executor.start_polling(dp)
