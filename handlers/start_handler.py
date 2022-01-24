import os
import sqlite_db
import markups as nav
from aiogram import types, Dispatcher

ADMIN_ID = int(os.environ["ADMIN_ID"])


# @dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    data_user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    if data_user[0] == ADMIN_ID:
        await sqlite_db.sql_add_user(data_user[0], data_user)
        await message.answer(f"Привет, выберите команду...", reply_markup=nav.adminMenu)
        await message.answer("Расписание проходящих автобусов", reply_markup=nav.inlineMenu)
    else:
        await sqlite_db.sql_add_user(data_user[0], data_user)
        await message.answer(f"Привет, выберите команду...", reply_markup=nav.userMenu)
        await message.answer("Расписание проходящих автобусов", reply_markup=nav.inlineMenu)


def register_handlers_all(dp : Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
