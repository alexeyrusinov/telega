import sqlite3 as sq
from func import pars_bus


def sql_start():
    with sq.connect("users.db") as con:
        cur = con.cursor()
        print("Data base connected Ok!")
        cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY,'
                    'user_name TEXT,'
                    'name TEXT,'
                    'passing_bus INT)')
        con.commit()
        cur.close()


async def sql_add_user(user_id, data_user):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}' ")
        data = cur.fetchone()
        print(f'data - {data}, попался - {data_user}')
        if data is None:
            # add values in fields
            cur.execute('INSERT INTO users VALUES(?, ?, ?, NULL)', data_user, )
            print(f'{data_user} добавлен в db')
            con.commit()
        else:
            print(f"{data_user}: уже существует в db")
        cur.close()


def get_all_users_db():
    with sq.connect("users.db") as con:
        cur = con.cursor()
        result = ''
        count = 0
        for value in cur.execute("SELECT ROWID, * FROM users"):
            count += 1
            result = result + str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + " " + str(value[3]) + " " + str(value[4]) + '\n'
        result = result + f'Всего пользователей: {count}'
        cur.close()
        print("get_all_users_db done")
        return result


def get_passing_bus(user_id):
    with sq.connect("users.db") as con:
        cur = con.cursor()
        sqlite_select = """SELECT passing_bus FROM users WHERE user_id = ?"""
        cur.execute(sqlite_select, (user_id,))
        result = cur.fetchone()
        cur.close()
        if result[0] is None:
            return f'Не выбран тип расписания, нажми: /select'
        else:
            match result[0]:
                case 1:
                    return pars_bus.get_all_bus_schedule()
                case 2:
                    return pars_bus.get_buses_dispatched()
                case 3:
                    return pars_bus.get_buses_canceled()
                case 4:
                    return pars_bus.get_current_schedule()


async def add_passing_bus(data_user, result):
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

