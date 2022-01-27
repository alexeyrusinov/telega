from aiogram import types, Dispatcher
import sqlite_db
import markups as nav
from create_bot import bot
import random
from func.pars_bus import get_all_bus_schedule, get_buses_dispatched, get_current_schedule, get_buses_canceled


# @dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    data_user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    # await sqlite_db.sql_add_user(data_user[0], data_user)
    await sqlite_db.sql_add_user(data_user)
    await message.answer("select command..", reply_markup=nav.user_and_admin_menu(message.from_user.id))


# @dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Подскажет тебе: @rusinov")
    print("Command help done")


# @dp.callback_query_handler(text="btnRandom")
async def get_random_num(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, "Случайное сисло: {0}".format(random.randint(0, 1000)), reply_markup=nav.myMenu)
    # await bot.edit_message_text("Случайное число: {0}".format(random.randint(0, 1000)), message.from_user.id, message_id = message.message.message_id)
    print("getRandomNum done")


# @dp.callback_query_handler(text_contains="bus")
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


# @dp.callback_query_handler(text_contains="buy")
async def bot_shop(call: types.CallbackQuery):  # это чтобы понять какая кнопка была нажата
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == "buySub":
        await bot.send_message(call.from_user.id, "Тарифы на подписку", reply_markup=nav.myMenu)
    elif call.data == "buyVip":
        await bot.send_message(call.from_user.id, "Купить VIP", reply_markup=nav.myMenu)
    print("botShop done")


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_callback_query_handler(get_random_num, text="btnRandom")
    dp.register_callback_query_handler(inline_menu, text_contains="bus")
    dp.register_callback_query_handler(bot_shop, text_contains="buy")

