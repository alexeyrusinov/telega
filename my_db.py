from aiogram import types
import json
import logging
import os
from func import pars_bus
import sqlite3 as sq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def sql_start():
    with sq.connect("files/users.db") as con:
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
    with sq.connect("files/users.db") as con:
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
    with sq.connect("files/users.db") as con:
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
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE users SET passing_bus = ? WHERE user_id = ?""", (result, data_user[0],))
        con.commit()
        cur.close()
        logger.info(f"value of column passing_bus of user {data_user} updated to {result}")


async def update_sp_and_fp_call(data_user, start_place_call, finish_place_call):
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT start_place_call, finish_place_call  FROM users WHERE user_id = ?""", (data_user[0],))
        items = cur.fetchall()
        if items[0][0] == start_place_call and items[0][1] == str(finish_place_call):
            logger.info(f"start_place_call - {start_place_call}, finish_place_call - {finish_place_call}")
        else:
            with sq.connect("files/users.db") as con:
                cur = con.cursor()
                cur.execute("""UPDATE users SET start_place_call = ?, finish_place_call = ?  WHERE user_id = ?""", (start_place_call, finish_place_call, data_user[0],))
                con.commit()
                logger.info(f"value of start_place_call = {start_place_call}  finish_place_call = {finish_place_call} of user {data_user}")
        cur.close()

# __________________________________


def load_file(file):
    with open(file) as f:  # Read json file
        stations = json.load(f)
        stations = dict(reversed(list(stations.items())))  # revers
    return stations


def create_table_start_place():
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        logger.info("table created :start_place")
        cur.execute('CREATE TABLE IF NOT EXISTS start_place(name_station TEXT PRIMARY KEY,'
                    'station_call TEXT)')
        con.commit()
        cur.close()


create_table_start_place()


def create_table_finish_place():
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        logger.info("table created :finish_place")
        cur.execute('CREATE TABLE IF NOT EXISTS finish_place(name_station_fp TEXT PRIMARY KEY,'
                    'name_station_lower_fp TEXT,'
                    'station_call_fp TEXT)')
        con.commit()
        cur.close()


create_table_finish_place()


def insert_start_station():
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        stations = load_file('files/starting_point_24.json')
        stations_k = []
        for k, v in reversed(stations.items()):
            stations_k.append((k, v))
        cur.executemany(
            "INSERT INTO start_place VALUES (?, ?)", stations_k)
        con.commit()
        cur.close()


# insert_start_station()

def insert_finish_station():
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        stations = load_file('files/704.json')
        stations_k = []
        for k, v in reversed(stations.items()):
            stations_k.append((k, k.lower(), v))
        cur.executemany(
            "INSERT INTO finish_place (name_station_fp, name_station_lower_fp, station_call_fp) VALUES (?, ?, ?)", stations_k)
        con.commit()
        cur.close()


# insert_finish_station()

