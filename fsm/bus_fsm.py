from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
import my_db
from mark import markups as nav
from handlers.client_handlers import send_welcome, send_help


class FSMSelectBus(StatesGroup):
    question = State()


# Задаём вопрос
async def fsm_start(message: types.Message):
    await my_db.sql_add_user(message)
    await FSMSelectBus.question.set()
    await message.reply("Выбери тип расписания:  ", reply_markup=nav.bus_answer_menu)


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")
    await send_welcome(message)


# ловим  ответ
async def load_question(message: types.Message, state: FSMContext):
    data_user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    async with state.proxy() as data:
        data["type_schedule"] = message.text
        result = data["type_schedule"]
        if result in ["все автобусы", "отправленные", "отмененные", "ближайшие"]:
            await my_db.update_type_timetable_passing_bus(data_user, result)
            await state.finish()
            if result == "все автобусы":
                # await message.reply(get_all_bus_schedule(id_station_arr=1331, days=0),
                #                     reply_markup=nav.user_and_admin_menu(message.from_user.id))
                await message.reply("Тип расписания изменён на: 'все автобусы'",
                                    reply_markup=nav.user_and_admin_menu(message.from_user.id))
            elif result == "отправленные":
                # await message.reply(get_bus_dispatched(id_station_arr=1331, days=0),
                #                     reply_markup=nav.user_and_admin_menu(message.from_user.id))
                await message.reply("Тип расписания изменён на: 'отправленные'",
                                    reply_markup=nav.user_and_admin_menu(message.from_user.id))
            elif result == "отмененные":
                # await message.reply(get_bus_canceled(id_station_arr=1331, days=0),
                #                     reply_markup=nav.user_and_admin_menu(message.from_user.id))
                await message.reply("Тип расписания изменён на: 'отмененные'",
                                    reply_markup=nav.user_and_admin_menu(message.from_user.id))
            elif result == "ближайшие":
                # await message.reply(get_current_schedule(id_station_arr=1331, days=0),
                #                     reply_markup=nav.user_and_admin_menu(message.from_user.id))
                await message.reply("Тип расписания изменён на: 'ближайшие'",
                                    reply_markup=nav.user_and_admin_menu(message.from_user.id))
        elif result == '/start':
            await state.finish()
            await send_welcome(message)
        elif result == '/help':
            await state.finish()
            await send_help(message)
        elif result == '/select':
            await state.reset_state()
            await fsm_start(message)


def register_handlers_bus_fsm(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands="select", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True, ), state="*")
    dp.register_message_handler(load_question, state=FSMSelectBus.question)
