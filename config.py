import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHEKICHAT = os.getenv("CHEKICHAT")
ADMINS = os.getenv("ADMINS").split(',')
manager = os.getenv("manager").split(',')
JSON_FILE = os.getenv("JSON_FILE")
