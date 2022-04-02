import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import sqlite3 as sq
import my_db
from func import pars_bus
from func.pars_bus import get_current_schedule
from mark import markups as nav
from aiogram.dispatcher import FSMContext
from create_bot import bot


def check_station(file):
    with open(file) as f:  # Read json file
        stations = json.load(f)
        stations_call = []
        for k, v in stations.items():
            stations_call.append(v)
    return stations_call


def get_station(value, file):
    with open(file) as f:  # Read json file
        stations = json.load(f)
    my_dict = {}
    for k, v in reversed(stations.items()):
        if value in k.upper():
            my_dict.update({k: v})
    return my_dict


def get_name_station(name_file, id_station):
    with open(name_file) as f:  # Read json file
        stations = json.load(f)
        for k, v in stations.items():
            if v == f'{id_station}':
                name_station = k
        return name_station


def load_file(file):
    with open(file) as f:  # Read json file
        stations = json.load(f)
        stations = dict(reversed(list(stations.items())))  # revers
    return stations


class FSMSelectStation(StatesGroup):
    start_place_question = State()
    start_place_check_answer = State()
    finish_place_question = State()


async def station_fsm_set(message: types.Message):
    await FSMSelectStation.start_place_question.set()
    await message.reply("Откуда: ", reply_markup=nav.generate_keyboard_station(load_file('files/starting_point_24.json'), 'start', 1))
    await message.answer("Выбирай..", reply_markup=nav.cancel_menu)


async def get_sp_and_fp_user_call(message: types.Message):
    with sq.connect("../users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT start_place_call, finish_place_call  FROM users WHERE user_id = ?""", (message.from_user.id,))
        result = cur.fetchall()
        cur.close()
        if result[0][0] == str(None) and result[0][1] == str(None):
            await station_fsm_set(message)
        else:
            await message.answer(pars_bus.get_current_schedule(result[0][0], result[0][1], days=0))


async def station_fsm_question_start_place(call: types.CallbackQuery, state: FSMContext):
    call_user_station = []
    user_answer = call.data.split()
    for word in user_answer:
        if word.isalpha():
            call_user_station.append(word)
    async with state.proxy() as data:
        data["start_place_user_call"] = call_user_station[0]
        data["start_place"] = get_name_station('files/starting_point_24.json', call_user_station[0])
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f"От автостации - {data['start_place']}")
    await bot.send_message(call.from_user.id, "Куда: (например: Екатеринбург) ", reply_markup=nav.cancel_menu)
    await FSMSelectStation.next()


async def station_fsm_question_finish_place(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["finish_place"] = message.text.upper()
    dict_with_result_station = get_station(data["finish_place"], 'files/704.json')
    if len(dict_with_result_station) == 0:
        await message.answer("Попробуй ещё..\nКуда: (например: Екатеринбург) ", reply_markup=nav.cancel_menu)
        await FSMSelectStation.start_place_check_answer.set()
    else:
        await message.answer("Какую из:", reply_markup=nav.generate_keyboard_station(dict_with_result_station, 'id', row_wight=1))
        await FSMSelectStation.next()


async def station_fsm_check_answer_finish_place(call: types.CallbackQuery, state: FSMContext):
    call_user_station = []
    user_answer = call.data.split()
    for word in user_answer:
        if word.isnumeric():
            call_user_station.append(int(word))
    async with state.proxy() as data:
        data["finish_place_user_call"] = call_user_station[0]
        start_place = data["start_place"]
        finish_place = get_name_station('files/704.json', call_user_station[0])
        start_call = data["start_place_user_call"]
        finish_call = data["finish_place_user_call"]
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f"*от* {start_place} *до* {finish_place}", reply_markup=nav.user_and_admin_menu(call.from_user.id), parse_mode="Markdown")
    await bot.send_message(call.from_user.id, f"{get_current_schedule(start_call, finish_call, days=0)}")
    data_user = (call.from_user.id, call.from_user.username, call.from_user.first_name)
    await my_db.update_sp_and_fp_call(data_user, start_call, finish_call)
    await state.finish()


def register_handlers_bus_station(dp: Dispatcher):
    dp.register_message_handler(get_sp_and_fp_user_call, text='Последнее расписание', state="*")
    dp.register_message_handler(station_fsm_set, text='Выбор направления', state="*")
    dp.register_callback_query_handler(station_fsm_question_start_place, text_contains="start", state=FSMSelectStation.start_place_question)
    dp.register_message_handler(station_fsm_question_finish_place, state=FSMSelectStation.start_place_check_answer)
    dp.register_callback_query_handler(station_fsm_check_answer_finish_place, text_contains="id", state=FSMSelectStation.finish_place_question)

