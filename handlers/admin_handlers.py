from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked
import sqlite3 as sq
import sqlite_db
from create_bot import bot, ADMIN_ID


# @dp.message_handler(commands=['send'])
async def send_message_all_users(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        with sq.connect("users.db") as con:
            cur = con.cursor()
            for user in cur.execute("SELECT user_id, name  FROM users"):
                user_id = "".join(map(str, str(user[0])))
                try:
                    await bot.send_message(user_id, message.text[6:])
                    print(f"text: \"{message.text[6:]}\" to - {user[1]} - {user[0]}")
                except BotBlocked:
                    print(f"user {user_id} - bot blocked")
            cur.close()
        print(f"Command send done, text: \"{message.text[6:]}\" ")
    else:
        await message.answer("only for admin")


async def get_all_users(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(message.from_user.id, sqlite_db.get_all_users_db())
    else:
        await message.answer("only for admin")


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(send_message_all_users, commands=['send'])
    dp.register_message_handler(get_all_users, text="alldb")