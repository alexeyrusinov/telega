import my_db
from aiogram import executor
from create_bot import dp
from handlers import client_handlers, admin_handlers, other_handlers
import fsm
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


fsm.bus_fsm.register_handlers_bus_fsm(dp)
fsm.sp_fp_fsm.register_handlers_bus_station(dp)
client_handlers.register_handlers_client(dp)
admin_handlers.register_handlers_admin(dp)
other_handlers.register_handlers_other(dp)


async def on_startup(_):
    logger.info("Bot is online!")
    my_db.sql_start()


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception:
        print("ooooops, maybe No internet connection")
        raise
