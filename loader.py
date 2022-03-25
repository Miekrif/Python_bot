from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from pathlib import Path
from dotenv import load_dotenv

from data import config

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.environ['TOKEN']

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)