from aiogram import Dispatcher, types
import sqlite3 as sq
import my_db
from fsm.sp_fp_fsm import station_fsm_set, get_name_station
from mark import markups as nav
from create_bot import bot, ADMIN_ID
from func import exchange_rate
from func.date_and_time import get_convert_date_time
from mark.markups import generation_date_schedule


async def filter_message(message: types.Message):
    if message.text == "Текущее время и дата":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id, get_convert_date_time())
    elif message.text == "Главное меню":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id, "Главное меню",
                               reply_markup=nav.user_and_admin_menu(message.from_user.id))
    elif message.text == "Другое":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id, "Другое", reply_markup=nav.otherMenu)
    elif message.text == "Exchange rate":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id,
                               exchange_rate.get_exchange_rate_from_api(11, 688, sign_dollar='$', sign_rubl='₽'),
                               parse_mode="Markdown")
    elif message.text == "BTC/USDT":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id, exchange_rate.get_exchange_rate(11, '$'), parse_mode="Markdown")
    elif message.text == "USDT/RUB":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id, exchange_rate.get_exchange_rate(688, '₽'), parse_mode="Markdown")
    elif message.text == "inlineButtons":
        await my_db.sql_add_user(message)
        await bot.send_message(message.from_user.id, "inlineButtons", reply_markup=nav.myMenu)
    elif message.text == "Расписание на ближайшие дни":
        await my_db.sql_add_user(message)
        data_user = message.from_user.id
        with sq.connect("files/users.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT start_place_call, finish_place_call  FROM users WHERE user_id = ?""", (data_user,))
            items = cur.fetchall()
            if items[0][0] == str(None) and items[0][1] == str(None):
                await station_fsm_set(message, flag_next_schedule=True)
            else:
                start_place = get_name_station('files/starting_point_24.json', items[0][0])
                finish_place = get_name_station('files/704.json', items[0][1])
                await message.answer(f"от *{start_place}* до *{finish_place}*",
                                     reply_markup=generation_date_schedule(start_place=items[0][0], finish_place=items[0][1]),
                                     parse_mode="Markdown")
    else:
        if message.from_user.id != ADMIN_ID:
            await my_db.sql_add_user(message)
            await bot.forward_message(ADMIN_ID, message.from_user.id, message.message_id)
        if message.from_user.id == ADMIN_ID:
            await my_db.sql_add_user(message)
            try:
                var = message.reply_to_message
                var = var["forward_from"]["id"]
                await bot.send_message(var, message.text)
            except TypeError:
                pass


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(filter_message)
