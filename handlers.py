import os
# import types
# from aiogram import Dispatcher
import markups as nav
import sqlite_db
# from start import dp
from aiogram import types, Dispatcher


ADMIN_ID = int(os.environ["ADMIN_ID"])


# @dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    data_user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    # if user_id == admin.ADMIN_ID:
    if user_id == ADMIN_ID:
        await sqlite_db.sql_add_command(user_id, data_user)
        await message.answer(f"Привет, выберите команду...", reply_markup=nav.adminMenu)
        await message.answer("Расписание проходящих автобусов", reply_markup=nav.inlineMenu)
    else:
        await sqlite_db.sql_add_command(user_id, data_user)
        await message.answer(f"Привет, выберите команду...", reply_markup=nav.userMenu)
        await message.answer("Расписание проходящих автобусов", reply_markup=nav.inlineMenu)


def register_handlers_all(dp : Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
