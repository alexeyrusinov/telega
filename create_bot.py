import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


ADMIN_ID = int(os.environ["ADMIN_ID"])
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))   # object bot
dp = Dispatcher(bot, storage=storage)