from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from func.pars_bus import get_current_schedule, get_all_bus_schedule,\
    get_buses_dispatched, get_buses_canceled
import os
import sqlite_db

ADMIN_ID = int(os.environ["ADMIN_ID"])


class FSMAdmin(StatesGroup):
    question = State()


#Задаём вопрос
# dp.message_handler(commands="Выбрать", state=None)
async def fsm_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMAdmin.question.set()
        await message.reply("Выберите тип расписания, отправив только цифру:\n"
                            "1 - Все автобусы,\n"
                            "2 - Отправленные,\n"
                            "3 - Отменённые,\n"
                            "4 - Ближайшие")
    else:
        await message.answer("sorry, only for admin")


#Выход из состояний
# @dp.message_handler(state="*", commands="отмена")
# @dp.message_handler(Text(equals"отмена", ignore_case=True,)state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


#ловим первый ответ
# dp.message_handler(state=FSMAdmin.question)
async def load_question(message: types.Message, state:FSMContext):
    user_id = message.from_user.id
    data_user = [message.from_user.id, message.from_user.username, message.from_user.first_name]
    async with state.proxy() as data:
        data["type_schedule"] = message.text
    async with state.proxy() as data:
        match data["type_schedule"]:
            case '1':
                await message.reply(get_all_bus_schedule())
            case '2':
                await message.reply(get_buses_dispatched())
            case '3':
                await message.reply(get_buses_canceled())
            case '4':
                await message.reply(get_current_schedule())
    result = int(data["type_schedule"])
    await sqlite_db.add_passing_bus(user_id, result)
    await state.finish()


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(fsm_start, commands="select", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True, ), state="*")
    dp.register_message_handler(load_question, state=FSMAdmin.question)



