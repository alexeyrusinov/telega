import sqlite_db
from aiogram import executor
from create_bot import dp
from handlers import client_handlers, admin_handlers, other_handlers
from fsm import bus_fsm


client_handlers.register_handlers_client(dp)
bus_fsm.register_handlers_bus_fsm(dp)
admin_handlers.register_handlers_admin(dp)
other_handlers.register_handlers_other(dp)


async def on_startup(_):
    print("Bot is online!")
    sqlite_db.sql_start()


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception:
        print("ooooops, No internet connection")
        raise
