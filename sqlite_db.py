import sqlite3 as sq


def sql_start():
    # global base, cur
    con = sq.connect("users.db")
    cur = con.cursor()
    if con:
        print("Data base connected Ok!")
        cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY, user_name TEXT, name TEXT, passing_bus INT)')
        con.commit()
    cur.close()
    con.close()


async def sql_add_command(user_id, data_user):
    con = sq.connect("users.db")
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
    con.close()


def get_all_users_db():
    con = sq.connect("users.db")
    cur = con.cursor()
    result = ''
    count = 0
    for value in cur.execute("SELECT ROWID, * FROM users"):
        count += 1
        result = result + str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + " " + str(value[3]) + " " + str(value[4]) + '\n'
    result = result + f'Всего пользователей: {count}'
    cur.close()
    con.close()
    print("get_all_users_db done")
    return result


async def add_passing_bus(user_id, result):
    con = sq.connect("users.db")
    cur = con.cursor()
    cur.execute("""UPDATE users SET passing_bus = ? WHERE user_id = ?""", (result, user_id,))
    print(f"value of column passing_bus of user {user_id} update to {result}")
    con.commit()
    cur.close()
    con.close()

# добавить удаление пользователя через машина состояний

# def dell_user_db():
#     base = sq.connect("users.db")
#     cur = base.cursor()
#     for user in cur.execute(f"DELETE FROM users WHERE ROWID = {user_number}"):

