from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked
import sqlite3 as sq
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, ADMIN_ID
from mark.markups import check_menu, user_and_admin_menu, cancel_menu
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


# del user with FSM
class FSMDelUserFromDB(StatesGroup):
    message_del = State()
    check_del = State()


async def send_question_del(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMDelUserFromDB.message_del.set()
        await message.reply("enter user_id of the user to be deleted..", reply_markup=cancel_menu)
    else:
        await message.answer("only for admin")


async def load_message_del(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        result = data["text"]
        with sq.connect("users.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (result,))
            data_user = cur.fetchall()
            if data_user:
                data["data_user"] = data_user
                await message.answer(f"are you sure to delete user:\n {data_user[0]}", reply_markup=check_menu)
            else:
                await message.answer("oops, maybe incorrect user_id")
                await send_question_del(message)
                await state.reset_state()
            cur.close()
    await FSMDelUserFromDB.next()


async def del_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = message.text
        user_id = data["text"]
        answer = data["answer"]
        data_user = data["data_user"]
        if answer == "верно":
            with sq.connect("users.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM users WHERE user_id = ? ", (user_id,))
                await state.finish()
                await message.answer(f"user: {data_user[0]} - was deleted",
                                     reply_markup=user_and_admin_menu(message.from_user.id))
                logger.info(f"user: {data_user[0]} - was deleted")
                con.commit()
                cur.close()
        else:
            await state.reset_state()
            await message.answer("canceled", reply_markup=user_and_admin_menu(message.from_user.id))


# send message to all users
class FSMSendMessageToAllUsers(StatesGroup):
    message_send = State()
    check_send = State()


# Задаём вопрос
async def send_question_send(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMSendMessageToAllUsers.message_send.set()
        await message.reply("enter a message for everyone..\n text only..", reply_markup=cancel_menu)
    else:
        await message.answer("only for admin")


async def load_message_send(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        result = data["text"]
        await message.answer(f"check before sending a message:\n {result}", reply_markup=check_menu)
    await FSMSendMessageToAllUsers.next()


async def send_message_all_users(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = message.text
        text = data["text"]
        answer = data["answer"]
        with sq.connect("users.db") as con:
            cur = con.cursor()
            for user in cur.execute("SELECT user_id, name  FROM users"):
                user_id = "".join(map(str, str(user[0])))
                try:
                    if answer == "верно":
                        await bot.send_message(user_id, text, reply_markup=user_and_admin_menu(message.from_user.id))
                        await state.finish()
                        logger.info(f"text: \"{text}\" send to - {user[1]} - {user[0]} - done")
                    else:
                        await state.reset_state()
                        await message.answer("отменено", reply_markup=user_and_admin_menu(message.from_user.id))
                        logger.info(f"command \"SendMessageToAllUsers\" NOT done, text: \"{text}\" ")
                        break
                except BotBlocked:
                    logger.info(f"user {user_id} - bot blocked")
            cur.close()


async def get_all_users(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        with sq.connect("users.db") as con:
            cur = con.cursor()
            result = ''
            count = 0
            for value in cur.execute("SELECT * FROM users"):
                count += 1
                result += str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + " " + str(value[3]) + '\n'
            result += f'total users: {count}'
            cur.close()
            logger.info(f"total users in db: {count}")
        await bot.send_message(message.from_user.id, result)
    else:
        await message.answer("only for admin")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(send_question_del, text='del', state=None)
    dp.register_message_handler(load_message_del, state=FSMDelUserFromDB.message_del)
    dp.register_message_handler(del_user, state=FSMDelUserFromDB.check_del)
    dp.register_message_handler(send_question_send, text='send', state=None)
    dp.register_message_handler(load_message_send, state=FSMSendMessageToAllUsers.message_send)
    dp.register_message_handler(send_message_all_users, state=FSMSendMessageToAllUsers.check_send)
    dp.register_message_handler(get_all_users, text="alldb")
