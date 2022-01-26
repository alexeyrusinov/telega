from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from func.pars_bus import get_current_schedule, get_all_bus_schedule,\
    get_buses_dispatched, get_buses_canceled
import sqlite_db
import markups as nav
from handlers.client_handlers import send_welcome


class FSMSelectBus(StatesGroup):
    question = State()


#Задаём вопрос
# dp.message_handler(commands="Выбрать", state=None)
async def fsm_start(message: types.Message):
    await FSMSelectBus.question.set()
    await message.reply("Выберите тип расписания, отправив только цифру:\n"
                        "1 - Все автобусы,\n"
                        "2 - Отправленные,\n"
                        "3 - Отменённые,\n"
                        "4 - Ближайшие", reply_markup=nav.bus_answer_menu)


#Выход из состояний
# @dp.message_handler(state="*", commands="отмена")
# @dp.message_handler(Text(equals"отмена", ignore_case=True,)state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")
    await send_welcome(message)


#ловим первый ответ
# dp.message_handler(state=FSMAdmin.question)
async def load_question(message: types.Message, state:FSMContext):
    data_user = [message.from_user.id, message.from_user.username, message.from_user.first_name]
    async with state.proxy() as data:
        data["type_schedule"] = message.text
        try:
            result = int(data["type_schedule"])
            if 0 < result <= 4:
                await sqlite_db.add_passing_bus(data_user, result)
                await state.finish()
                match result:
                    case 1:
                        await message.reply(get_all_bus_schedule(), reply_markup=nav.user_and_admin_menu(message.from_user.id))
                    case 2:
                        await message.reply(get_buses_dispatched(), reply_markup=nav.user_and_admin_menu(message.from_user.id))
                    case 3:
                        await message.reply(get_buses_canceled(), reply_markup=nav.user_and_admin_menu(message.from_user.id))
                    case 4:
                        await message.reply(get_current_schedule(), reply_markup=nav.user_and_admin_menu(message.from_user.id))
                # await send_welcome(message)
            else:
                await state.reset_state()
                await message.answer("Только цифру из предложенных...")
                await fsm_start(message)
        except ValueError:
            await state.reset_state()
            await message.answer("Только цифру, а не это ваше...")
            await fsm_start(message)


def register_handlers_bus_fsm(dp : Dispatcher):
    dp.register_message_handler(fsm_start, commands="select", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True, ), state="*")
    dp.register_message_handler(load_question, state=FSMSelectBus.question)



