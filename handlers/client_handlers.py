from aiogram import types, Dispatcher
import logging
import my_db
from func.bus_func import get_schedule_with_type
from mark import markups as nav
from create_bot import bot
import random
import os
import sqlite3 as sq


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


async def send_welcome(message: types.Message):
    await my_db.sql_add_user(message)
    await message.answer("Выбери команду..", reply_markup=nav.user_and_admin_menu(message.from_user.id))


async def send_help(message: types.Message):
    await my_db.sql_add_user(message)
    await message.answer("Подскажет тебе: @rusinov", reply_markup=None)


async def test_generate_inline_menu(call: types.CallbackQuery):
    day = int(call.data[:2])
    data_user = call.from_user.id

    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT start_place_call, finish_place_call, type_schedule  FROM users WHERE user_id = ?""", (data_user,))
        items = cur.fetchall()
        for i in range(day + 1):
            if i == day:
                await bot.delete_message(call.from_user.id, call.message.message_id)
                await bot.send_message(call.from_user.id,
                                       get_schedule_with_type(items[0][0], items[0][1], days=i, type_schedule=items[0][2]),
                                       parse_mode="Markdown")
                logger.info(f"call data: {call.data}, user: {call.from_user.username} - {call.from_user.first_name}")


async def get_random_num(message: types.Message):
    # await bot.delete_message(message.from_user.id, message.message.message_id)
    # await bot.send_message(message.from_user.id, "Случайное сисло: {0}".format(random.randint(0, 1000)),
    # reply_markup=nav.myMenu)
    await my_db.sql_add_user(message)
    await bot.edit_message_text("Случайное число: {0}".format(random.randint(0, 1000)),
                                message.from_user.id, message_id=message.message.message_id, reply_markup=nav.myMenu)


async def bot_shop(call: types.CallbackQuery):  # это чтобы понять какая кнопка была нажата
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == "buySub":
        await bot.send_message(call.from_user.id, "Тарифы на подписку", reply_markup=nav.myMenu)
    elif call.data == "buyVip":
        await bot.send_message(call.from_user.id, "Купить VIP", reply_markup=nav.myMenu)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_callback_query_handler(test_generate_inline_menu, text_contains=["day"])
    dp.register_callback_query_handler(get_random_num, text="btnRandom")
    dp.register_callback_query_handler(bot_shop, text_contains="buy")
