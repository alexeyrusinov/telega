import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from func.pars_bus import get_current_schedule
from mark import markups as nav
from aiogram.dispatcher import FSMContext
from create_bot import bot


def get_station(value):
    with open('files/704.json') as f:  # Read json file
        stations = json.load(f)
    my_dict = {}
    for k, v in stations.items():
        if value in k or value in k.casefold():
            my_dict.update({k: v})
    return my_dict


user_data = {}


class FSMSelectStation(StatesGroup):
    question = State()
    check_answer = State()


async def station_fsm_set(message: types.Message):
    user_data[message.from_user.id] = ""
    await message.reply("Введи место прибытия: ", reply_markup=nav.cancel_menu)
    await FSMSelectStation.question.set()


async def station_fsm_question(message: types.Message, state: FSMContext):
    user_data[message.from_user.id] = message.text
    result = get_station(user_data[message.from_user.id])
    if len(result) == 0:
        await message.answer("Попробуй ещё")
        await state.reset_state()
        await station_fsm_set(message)
    else:
        await message.answer("Какую из..", reply_markup=nav.generate_keyboard_station(result))
        await FSMSelectStation.next()


async def station_fsm_check_answer(call: types.CallbackQuery, state: FSMContext):
    result = []
    user_answer = call.data.split()
    for word in user_answer:
        if word.isnumeric():
            result.append(int(word))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, get_current_schedule(result[0], days=0), reply_markup=nav.user_and_admin_menu(call.from_user.id))
    await state.finish()


def register_handlers_bus_station(dp: Dispatcher):
    dp.register_message_handler(station_fsm_set, text='Расписание', state="*")
    dp.register_message_handler(station_fsm_question, state=FSMSelectStation.question)
    dp.register_callback_query_handler(station_fsm_check_answer, text_contains=" id", state=FSMSelectStation.check_answer)
