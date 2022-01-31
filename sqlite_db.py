from func import pars_bus
import sqlite3 as sq
from aiogram import types


def sql_start():
    with sq.connect("users.db") as con:
        cur = con.cursor()
        print("Data base connected Ok!")
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
            print(f'{data_user} - добавлен в db')
            con.commit()
        else:
            print(f"{data_user} - уже существует в db")
        cur.close()


def get_all_users_db():
    with sq.connect("users.db") as con:
        cur = con.cursor()
        result = ''
        count = 0
        for value in cur.execute("SELECT * FROM users"):
            count += 1
            result += str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + " " + str(value[3]) + '\n'
        result += f'Всего пользователей: {count}'
        cur.close()
        print("get_all_users_db done")
        return result


def get_timetable_passing_bus(user_id):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT passing_bus FROM users WHERE user_id = ?""", (user_id,))
        result = cur.fetchone()
        cur.close()
        match result[0]:
            case "все автобусы":
                return pars_bus.get_all_bus_schedule()
            case "отправленные":
                return pars_bus.get_buses_dispatched()
            case "отмененные":
                return pars_bus.get_buses_canceled()
            case "ближайшие":
                return pars_bus.get_current_schedule()


async def update_type_timetable_passing_bus(data_user, result):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE users SET passing_bus = ? WHERE user_id = ?""", (result, data_user[0],))
        con.commit()
        cur.close()
        print(f"value of column passing_bus of {data_user} update to {result}")


# добавить удаление пользователя через машина состояний

# def dell_user_db():
#     base = sq.connect("users.db")
#     cur = base.cursor()
#     for user in cur.execute(f"DELETE FROM users WHERE ROWID = {user_number}"):

