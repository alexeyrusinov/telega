from func import get_time, pars_bus, get_json_btc_usdt, url_binance
import markups as nav
from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite_db
import sqlite3 as sq


TOKEN = os.environ["TOKEN"]  # create variable environment


bot = Bot(TOKEN)  # object bot
dp = Dispatcher(bot)


async def on_startup(_):
    print("Bot is online!")
    sqlite_db.sql_start()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    data_user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    await sqlite_db.sql_add_command(user_id, data_user)
    await message.answer(f"Привет, выберите команду...", reply_markup= nav.mainMenu)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Подскажет тебе: @rusinov")


@dp.message_handler(commands=['send'])
async def send_message_all(message: types.Message):
    base = sq.connect("users.db")
    cur = base.cursor()
    for user in cur.execute("SELECT user_id FROM users"):
        user_id = "".join(user)
        await bot.send_message(user_id, message.text[6:])


@dp.message_handler()
async def echo_message(message: types.Message):
    #  await bot.send_message(message.from_user., message.text)  - тут реализовать отправку сообщения админу от других людей
    if message.text == "Текущее время и дата":
        await bot.send_message(message.from_user.id, get_time())
    elif message.text == "Главное меню":
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup = nav.mainMenu)
    elif message.text == "Другое":
        await bot.send_message(message.from_user.id, "Другое", reply_markup = nav.otherMenu)
    elif message.text == "all db":
        await bot.send_message(message.from_user.id, sqlite_db.get_all_db())
    elif message.text == "Расписание автобуса":
        await bot.send_message(message.from_user.id, pars_bus())
    elif message.text == "Курс биткоина":
        await bot.send_message(message.from_user.id, get_json_btc_usdt(url_binance))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)