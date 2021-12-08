from key import token, url_binance
from func import get_time, get_json_btcusdt, pars_bus
import markups as nav
import datetime
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token) # обьект бота
dp = Dispatcher(bot)


now = datetime.datetime.now()
now_day_time = now.strftime("%H:%M %A %d/%m/%y")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Привет, выбери команду...", reply_markup= nav.mainMenu)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer("Подскажет тебе: @rusinov")


@dp.message_handler()
async def echo_message(message: types.Message):
    if message.text == "Текущее время и дата":
        await bot.send_message(message.from_user.id, get_time())
    elif message.text == "Главное меню":
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup = nav.mainMenu)
    elif message.text == "Другое":
        await bot.send_message(message.from_user.id, "Другое", reply_markup = nav.otherMenu)
    elif message.text == "Расписание автобуса":
        await bot.send_message(message.from_user.id, pars_bus())
    elif message.text == "Курс биткоина":
        await bot.send_message(message.from_user.id, get_json_btcusdt(url_binance))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)