from token import token
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token) # обьект бота

dp = Dispatcher(Bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)