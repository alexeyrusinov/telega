from func import pars_bus
import sqlite3 as sq
from aiogram import types
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def sql_start():
    with sq.connect("../users.db") as con:
        cur = con.cursor()
        logger.info("Data base connected Ok!")
        cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY,'
                    'user_name TEXT,'
                    'name TEXT,'
                    # 'passing_bus TEXT DEFAULT "ближайшие")')
                    'start_place_call TEXT DEFAULT "None",'
                    'finish_place_call TEXT TEXT DEFAULT "None")')
        con.commit()
        cur.close()


async def sql_add_user(message: types.Message):
    with sq.connect("../users.db") as con:
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


def get_timetable_passing_bus(user_id, id_station_arr, days):
    with sq.connect("../users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT passing_bus FROM users WHERE user_id = ?""", (user_id,))
        result = cur.fetchone()
        cur.close()
        if result[0] == "все автобусы":
            return pars_bus.get_all_bus_schedule(id_station_arr, days)
        elif result[0] == "отправленные":
            return pars_bus.get_bus_dispatched(id_station_arr, days)
        elif result[0] == "отмененные":
            return pars_bus.get_bus_canceled(id_station_arr, days)
        elif result[0] == "ближайшие":
            return pars_bus.get_current_schedule(id_station_arr, days)
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
    with sq.connect("../users.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE users SET passing_bus = ? WHERE user_id = ?""", (result, data_user[0],))
        con.commit()
        cur.close()
        logger.info(f"value of column passing_bus of user {data_user} updated to {result}")


async def update_sp_and_fp_call(data_user, start_place_call, finish_place_call):
    with sq.connect("../users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT start_place_call, finish_place_call  FROM users WHERE user_id = ?""", (data_user[0],))
        items = cur.fetchall()
        if items[0][0] == start_place_call and items[0][1] == str(finish_place_call):
            logger.info(f"start_place_call - {start_place_call}, finish_place_call - {finish_place_call}")
        else:
            with sq.connect("../users.db") as con:
                cur = con.cursor()
                cur.execute("""UPDATE users SET start_place_call = ?, finish_place_call = ?  WHERE user_id = ?""", (start_place_call, finish_place_call, data_user[0],))
                con.commit()
                logger.info(f"value of start_place_call = {start_place_call}  finish_place_call = {finish_place_call} of user {data_user}")
        cur.close()


# def get_sp_and_fp_user_call(message: types.Message, user_id, days):
#     with sq.connect("../users.db") as con:
#         cur = con.cursor()
#         cur.execute("""SELECT start_place_call, finish_place_call  FROM users WHERE user_id = ?""", (user_id,))
#         result = cur.fetchall()
#         cur.close()
#         print(type(result))
#         print(result)
#         if result[0][0] and result[0][1]:
#             return pars_bus.get_current_schedule(result[0][0], result[0][1], days)
#         # if result:
#         #     return pars_bus.get_current_schedule(result[0][0], result[0][1], days)
#         else:
#             station_fsm_set(message) # --------

        # elif result:
        #     return pars_bus.get_current_schedule(result[0][0], result[0][1], days)


