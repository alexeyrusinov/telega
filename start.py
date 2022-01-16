from pars_bus import get_btc_usdt_rate, get_current_schedule, get_all_bus_schedule,\
    get_buses_dispatched, get_buses_canceled
from date_and_time import get_convert_date_time
import sqlite_db
import markups as nav
from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3 as sq
import random

TOKEN = os.environ["TOKEN"]  # create variable environment
ADMIN_ID = os.environ["ADMIN_ID"]


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
    await message.answer(f"Привет, выберите команду...", reply_markup=nav.mainMenu)
    await message.answer("Расписание проходящих автобусов", reply_markup=nav.inlineMenu)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Подскажет тебе: @rusinov")
    print("Command help done")


@dp.message_handler(commands=['send'])
async def send_message_all_users(message: types.Message):
    base = sq.connect("users.db")
    cur = base.cursor()
    for user in cur.execute("SELECT user_id FROM users"):
        user_id = "".join(user)
        await bot.send_message(user_id, message.text[6:])
    print("Command send done")


@dp.callback_query_handler(text="btnRandom")
async def get_random_num(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, "Случайное сисло: {0}".format(random.randint(0, 1000)), reply_markup= nav.myMenu)
    # await bot.edit_message_text("Случайное число: {0}".format(random.randint(0, 1000)), message.from_user.id, message_id = message.message.message_id)
    print("getRandomNum done")


@dp.callback_query_handler(text_contains="bus")
async def inline_menu(call: types.CallbackQuery): # это чтобы понять какая кнопка была нажата
    data_user = (call.from_user.id, call.from_user.username, call.from_user.first_name)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == "all_buses":
        await bot.send_message(call.from_user.id, f"Все автобусы:\n {get_all_bus_schedule()}", reply_markup=nav.inlineMenu)
        print("inline Все автобусы done")
    elif call.data == "dispatched_buses":
        await bot.send_message(call.from_user.id, f"Отправленные:\n {get_buses_dispatched()}",
                               reply_markup=nav.inlineMenu)
        print("inline Отправленные автобусы done")
    elif call.data == "bus_schedule":
        await bot.send_message(call.from_user.id, f"Ближайшие:\n {get_current_schedule()}", reply_markup=nav.inlineMenu)
        print("inline Расписание done")
    elif call.data == "buses_canceled":
        await bot.send_message(call.from_user.id, f"Отменённые:\n {get_buses_canceled()}", reply_markup=nav.inlineMenu)
        print("inline Отменённые автобусы done")


@dp.callback_query_handler(text_contains="buy")
async def bot_shop(call: types.CallbackQuery): # это чтобы понять какая кнопка была нажата
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == "buySub":
        await bot.send_message(call.from_user.id, "Тарифы на подписку", reply_markup= nav.myMenu)
    elif call.data == "buyVip":
        await bot.send_message(call.from_user.id, "Купить VIP", reply_markup= nav.myMenu)
    print("botShop done")


@dp.message_handler()
async def echo_message(message: types.Message):
    # data_user = (call.from_user.id, call.from_user.username, call.from_user.first_name) ---- if need
    if message.text == "Текущее время и дата":
        await bot.send_message(message.from_user.id, get_convert_date_time())
    elif message.text == "Главное меню":
        await bot.send_message(message.from_user.id, "Главное меню", reply_markup=nav.mainMenu)
    elif message.text == "Другое":
        await bot.send_message(message.from_user.id, "Другое", reply_markup=nav.otherMenu)
    elif message.text == "all db":
        await bot.send_message(message.from_user.id, sqlite_db.get_all_users_db())
    elif message.text == "Расписание автобуса":
        await bot.send_message(message.from_user.id, get_current_schedule())
    elif message.text == "Курс биткоина":
        await bot.send_message(message.from_user.id, get_btc_usdt_rate())
    elif message.text == "inlineButtons":
        await bot.send_message(message.from_user.id, "inlineButtons", reply_markup=nav.myMenu)
    elif message.text is not None:
        await bot.send_message(ADMIN_ID, message.text)


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception:
        print("ooooops, No internet connection")