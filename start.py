from key import token
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token) # обьект бота

dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi! I'm EchoBot!")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer("Он поможет тебе: @rusinov")

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)