from aiogram import types, Dispatcher


# @dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Подскажет тебе: @rusinov")
    print("Command help done")


def register_handlers_help(dp : Dispatcher):
    dp.register_message_handler(send_help, commands=['help'])