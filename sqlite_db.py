import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("users.db")
    cur = base.cursor()
    if base:
        print("Data base connected Ok!")
    base.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, user_name TEXT, name TEXT)')
    base.commit()


async def sql_add_command(user_id, data_user):
    cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}' ")
    data = cur.fetchone()
    print(f'data - {data}\n'
          f'попался - {data_user}')
    if data is None:
        # add values in fields
        cur.execute('INSERT INTO users VALUES(?, ?, ?)', tuple(data_user))
        print(f'{data_user} добавлен в db')
        base.commit()
    else:
        print(f"{data_user}: уже существует в db")


def get_all_db():
    base = sq.connect("users.db")
    cur = base.cursor()
    result = ''
    count = 0
    for value in cur.execute("SELECT ROWID, * FROM users"):
        count += 1
        result = result + str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + " " + str(value[3]) + '\n'
    result = result + f'Всего пользователей: {count}'
    return result
