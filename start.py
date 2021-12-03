from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token = "5049775754:AAFRWJM6XCcYsFQtMDQTkVcJlmJnmSR5YJY") # обьект бота

dp = Dispatcher(Bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)