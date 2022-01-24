from func.pars_bus import get_current_schedule, get_all_bus_schedule, \
    get_buses_dispatched, get_buses_canceled
from func.date_and_time import get_convert_date_time
from func import btc
import sqlite_db
import markups as nav
from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3 as sq
import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # позволяет хранить данные в опер. памяти
import admin
from handlers import start_handler
from aiogram.utils.exceptions import BotBlocked


TOKEN = os.environ["TOKEN"]  # create variable environment
# ADMIN_ID = int(os.environ["ADMIN_ID"])
storage = MemoryStorage()
bot = Bot(TOKEN)  # object bot
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print("Bot is online!")
    sqlite_db.sql_start()


start_handler.register_handlers_all(dp)
admin.register_handlers_admin(dp)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Подскажет тебе: @rusinov")
    print("Command help done")


@dp.message_handler(commands=['send'])
async def send_message_all_users(message: types.Message):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        for user in cur.execute("SELECT user_id FROM users"):
            user_id = "".join(map(str, user))
            try:
                await bot.send_message(user_id, message.text[6:])
            except BotBlocked:
                print(f"user {user_id} - bot blocked")
        cur.close()
    print(f"Command send done, text: \"{message.text[6:]}\" ")


@dp.callback_query_handler(text="btnRandom")
async def get_random_num(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, "Случайное сисло: {0}".format(random.randint(0, 1000)),
                           reply_markup=nav.myMenu)
    # await bot.edit_message_text("Случайное число: {0}".format(random.randint(0, 1000)), message.from_user.id, message_id = message.message.message_id)
    print("getRandomNum done")


@dp.callback_query_handler(text_contains="bus")
async def inline_menu(call: types.CallbackQuery):  # это чтобы понять какая кнопка была нажата
    data_user = (call.from_user.id, call.from_user.username, call.from_user.first_name)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    match call.data:
        case "all_buses":
            await bot.send_message(call.from_user.id, f"Все автобусы:\n {get_all_bus_schedule()}",
                                   reply_markup=nav.inlineMenu)
            print("inline Все автобусы done")
        case "dispatched_buses":
            await bot.send_message(call.from_user.id, f"Отправленные:\n {get_buses_dispatched()}",
                                   reply_markup=nav.inlineMenu)
            print("inline Отправленные автобусы done")
        case "bus_schedule":
            await bot.send_message(call.from_user.id, f"Ближайшие:\n {get_current_schedule()}",
                                   reply_markup=nav.inlineMenu)
            print("inline Расписание done")
        case "buses_canceled":
            await bot.send_message(call.from_user.id, f"Отменённые:\n {get_buses_canceled()}",
                                   reply_markup=nav.inlineMenu)
            print("inline Отменённые автобусы done")


@dp.callback_query_handler(text_contains="buy")
async def bot_shop(call: types.CallbackQuery):  # это чтобы понять какая кнопка была нажата
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == "buySub":
        await bot.send_message(call.from_user.id, "Тарифы на подписку", reply_markup=nav.myMenu)
    elif call.data == "buyVip":
        await bot.send_message(call.from_user.id, "Купить VIP", reply_markup=nav.myMenu)
    print("botShop done")


@dp.message_handler()
async def echo_message(message: types.Message):
    match message.text:
        case "Текущее время и дата":
            await bot.send_message(message.from_user.id, get_convert_date_time())
        case "Главное меню":
            if message.from_user.id == start_handler.ADMIN_ID:
                await bot.send_message(message.from_user.id, "Главное меню", reply_markup=nav.adminMenu)
            else:
                await bot.send_message(message.from_user.id, "Главное меню", reply_markup=nav.userMenu)
        case "Другое":
            await bot.send_message(message.from_user.id, "Другое", reply_markup=nav.otherMenu)
        case "all db":
            if message.from_user.id == start_handler.ADMIN_ID:
                await bot.send_message(message.from_user.id, sqlite_db.get_all_users_db())
            else:
                await message.answer("only for admin")
        case "Расписание автобуса":
            # await bot.send_message(message.from_user.id, get_current_schedule())
            await bot.send_message(message.from_user.id, sqlite_db.get_passing_bus(message.from_user.id))
        case "Курс биткоина":
            await bot.send_message(message.from_user.id, btc.get_btc_usdt_rate())
        case "inlineButtons":
            await bot.send_message(message.from_user.id, "inlineButtons", reply_markup=nav.myMenu)
        case _:
            if message.from_user.id != start_handler.ADMIN_ID:
                await bot.forward_message(start_handler.ADMIN_ID, message.from_user.id, message.message_id)
            if message.from_user.id == start_handler.ADMIN_ID:
                try:
                    var = message.reply_to_message
                    var = var["forward_from"]["id"]
                    await bot.send_message(var, message.text)
                except TypeError:
                    pass


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception:
        print("ooooops, No internet connection")
        raise
