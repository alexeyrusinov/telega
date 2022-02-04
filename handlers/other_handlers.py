from aiogram import Dispatcher, types
import markups as nav
import sqlite_db
from create_bot import bot, ADMIN_ID
from func import btc
from func.date_and_time import get_convert_date_time


# @dp.message_handler()
async def filter_message(message: types.Message):
    match message.text:
        case "Текущее время и дата":
            await bot.send_message(message.from_user.id, get_convert_date_time())
        case "Главное меню":
            await bot.send_message(message.from_user.id, "Главное меню", reply_markup=nav.user_and_admin_menu(message.from_user.id))
        case "Другое":
            await bot.send_message(message.from_user.id, "Другое", reply_markup=nav.otherMenu)
        case "Расписание автобуса":
            await bot.send_message(message.from_user.id, sqlite_db.get_timetable_passing_bus(message.from_user.id))
        case "Курс биткоина":
            await bot.send_message(message.from_user.id, btc.get_btc_usdt_rate())
        case "inlineButtons":
            await bot.send_message(message.from_user.id, "inlineButtons", reply_markup=nav.myMenu)
        case _:
            if message.from_user.id != ADMIN_ID:
                await bot.forward_message(ADMIN_ID, message.from_user.id, message.message_id)
            if message.from_user.id == ADMIN_ID:
                try:
                    var = message.reply_to_message
                    var = var["forward_from"]["id"]
                    await bot.send_message(var, message.text)
                except TypeError:
                    pass


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(filter_message)
