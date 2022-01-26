from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked
import sqlite3 as sq
import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
from create_bot import bot, ADMIN_ID
from markups import check_menu, user_and_admin_menu


class FSMSendMessageToAllUsers(StatesGroup):
    message = State()
    check = State()


# Задаём вопрос
async def send_question(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMSendMessageToAllUsers.message.set()
        await message.reply("Введи сообщение для всех...")
    else:
        await message.answer("only for admin")


async def load_message(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        result = data["text"]
        await message.answer(f"Проверка перед отправкой:\n {result}", reply_markup=check_menu)
    await FSMSendMessageToAllUsers.next()


async def send_message_all_users(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data["answer"] = message.text
        text = data["text"]
        answer = data["answer"]
        with sq.connect("users.db") as con:
            cur = con.cursor()
            for user in cur.execute("SELECT user_id, name  FROM users"):
                user_id = "".join(map(str, str(user[0])))
                try:
                    if answer == "отправляем":
                        await bot.send_message(user_id, text, reply_markup=user_and_admin_menu(message.from_user.id))
                        await state.finish()
                        print(f"text: \"{text}\" to - {user[1]} - {user[0]} - done")
                    else:
                        await state.reset_state()
                        await message.answer("отменено", reply_markup=user_and_admin_menu(message.from_user.id))
                        print(f"сommand \"SendMessageToAllUsers\" NOT done, text: \"{text}\" ")
                        break
                except BotBlocked:
                    print(f"user {user_id} - bot blocked")
            cur.close()


async def get_all_users(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(message.from_user.id, sqlite_db.get_all_users_db())
    else:
        await message.answer("only for admin")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(send_question, commands=['send'], state=None)
    dp.register_message_handler(load_message, state=FSMSendMessageToAllUsers.message)
    dp.register_message_handler(send_message_all_users, state=FSMSendMessageToAllUsers.check)
    dp.register_message_handler(get_all_users, text="alldb")
