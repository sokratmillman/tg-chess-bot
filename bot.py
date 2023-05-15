from os import environ as env

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = env['API_TOKEN']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
