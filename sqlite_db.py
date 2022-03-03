from func import pars_bus
import sqlite3 as sq
from aiogram import types
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def sql_start():
    with sq.connect("users.db") as con:
        cur = con.cursor()
        logger.info("Data base connected Ok!")
        cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY,'
                    'user_name TEXT,'
                    'name TEXT,'
                    'passing_bus TEXT DEFAULT "ближайшие")')
        con.commit()
        cur.close()


async def sql_add_user(message: types.Message):
    with sq.connect("users.db") as con:
        data_user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE user_id = ?", (data_user[0],))
        data = cur.fetchone()
        if data is None:
            cur.execute('INSERT INTO users (user_id, user_name, name) VALUES(?, ?, ?)', data_user,)
            logger.info(f'{data_user} - added to db')
            con.commit()
        else:
            logger.info(f"{data_user} - already exists in db")
        cur.close()


def get_timetable_passing_bus(user_id, days=0):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT passing_bus FROM users WHERE user_id = ?""", (user_id,))
        result = cur.fetchone()
        cur.close()
        if result[0] == "все автобусы":
            return pars_bus.get_all_bus_schedule()
        elif result[0] == "отправленные":
            return pars_bus.get_bus_dispatched()
        elif result[0] == "отмененные":
            return pars_bus.get_bus_canceled()
        elif result[0] == "ближайшие":
            return pars_bus.get_current_schedule(days)
        # match result[0]:
        #     case "все автобусы":
        #         return pars_bus.get_all_bus_schedule()
        #     case "отправленные":
        #         return pars_bus.get_bus_dispatched()
        #     case "отмененные":
        #         return pars_bus.get_bus_canceled()
        #     case "ближайшие":
        #         return pars_bus.get_current_schedule(days)


async def update_type_timetable_passing_bus(data_user, result):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE users SET passing_bus = ? WHERE user_id = ?""", (result, data_user[0],))
        con.commit()
        cur.close()
        logger.info(f"value of column passing_bus of user {data_user} updated to {result}")

