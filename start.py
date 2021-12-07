from key import token, url_binance
import markups as nav
import datetime, requests
from aiogram import Bot, Dispatcher, executor, types
from btcusdt import get_json_btcusdt


bot = Bot(token) # обьект бота
dp = Dispatcher(bot)


now = datetime.datetime.now()
now_day_time = now.strftime("%H:%M %A %d/%m/%y")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Hi, I'm echo bot!", reply_markup= nav.mainMenu)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer("Он поможет тебе: @rusinov")


@dp.message_handler()
async def echo_message(message: types.Message):
    # await bot.send_message(msg.from_user.id, msg.text)
    if message.text == "Текущее время и дата":
        await bot.send_message(message.from_user.id, now_day_time)
    elif message.text == "Главное меню":
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup = nav.mainMenu)
    elif message.text == "Другое":
        await bot.send_message(message.from_user.id, "Другое", reply_markup = nav.otherMenu)
    elif message.text == "Информация":
        await bot.send_message(message.from_user.id, "Какая-то информация...")
    elif message.text == "Курс биткоина":
        await bot.send_message(message.from_user.id, get_json_btcusdt(url_binance))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)