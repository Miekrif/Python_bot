from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import text, quote_html
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config.config import BOT_TOKEN

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Включаем логгирование
dp.middleware.setup(LoggingMiddleware())
