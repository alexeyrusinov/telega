from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import math
import sqlite3 as sq
import my_db
from func import pars_bus
from func.pars_bus import get_current_schedule
from mark import markups as nav
from create_bot import bot

# user_data = {}


def get_keyboard_fab(page=1, elem_on_page=6):
    all_items = 24
    max_page = math.ceil(all_items / elem_on_page)
    skip = (page - 1) * elem_on_page

    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM start_place LIMIT %s OFFSET %s" % (elem_on_page, skip))
        items = cur.fetchall()
        cur.close()

    result_stations = []
    for i in items:
        result_stations.append(types.InlineKeyboardButton(text=i[0], callback_data=f"station-call-{i[1]}"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(*result_stations)

    service_buttons = list()
    keyboard.row_width = 3
    if page == 1:
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data="None"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}/{max_page}", callback_data="None"))
        if len(result_stations) < elem_on_page:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
        else:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="page-lib-2"))
    elif len(result_stations) < elem_on_page:
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data=f"page-lib-{page-1}"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}/{max_page}", callback_data="None"))
        service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
    else:
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data=f"page-lib-{page-1}"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}/{max_page}", callback_data="None"))
        if page < max_page:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data=f"page-lib-{page + 1}"))
        else:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
    keyboard.add(*service_buttons)
    return keyboard


async def update_keyboard_fab(message: types.Message, page: int):
    with suppress(MessageNotModified):
        await message.edit_reply_markup(reply_markup=get_keyboard_fab(page=page))
        # print(user_data)


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
    # await message.reply("Откуда: ", reply_markup=nav.generate_keyboard_station(load_file('files/starting_point_24.json'), 'start', 1))
    await message.reply("Откуда: ", reply_markup=get_keyboard_fab())
    await message.answer("Выбирай..", reply_markup=nav.cancel_menu)


# @dp.callback_query_handler(text_contains="page-lib-")
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
async def callbacks_num_change_fab(call: types.CallbackQuery):
    page = int(call.data[-1])
    # user_data[call.from_user.id] = page
    await update_keyboard_fab(call.message, page)
    await call.answer()


# @dp.callback_query_handler(text_contains="station-call-")
# async def callbacks_num_finish_fab(call: types.CallbackQuery):
#     print(call.data)
#     await call.answer()


async def get_sp_and_fp_user_call(message: types.Message):
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT start_place_call, finish_place_call  FROM users WHERE user_id = ?""", (message.from_user.id,))
        result = cur.fetchall()
        cur.close()
        if result[0][0] == str(None) and result[0][1] == str(None):
            await station_fsm_set(message)
        else:
            start_place = get_name_station('files/starting_point_24.json', result[0][0])
            finish_place = get_name_station('files/704.json', result[0][1])
            await message.answer(f"от *{start_place}* до *{finish_place}*", parse_mode="Markdown")
            await message.answer(pars_bus.get_current_schedule(result[0][0], result[0][1], days=0))


async def station_fsm_question_start_place(call: types.CallbackQuery, state: FSMContext):
    call_user_station = []
    user_answer = call.data.split('-')
    for word in user_answer:
        if word.isalpha():
            call_user_station.append(word)
    async with state.proxy() as data:
        data["start_place_user_call"] = call_user_station[2]
        data["start_place"] = get_name_station('files/starting_point_24.json', data["start_place_user_call"])
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, f"От автостации - {data['start_place']}")
    await bot.send_message(call.from_user.id, "Куда: (например: Екатеринбург) ", reply_markup=nav.cancel_menu)
    await call.answer()
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
    await call.answer()
    await state.finish()


def register_handlers_bus_station(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_num_change_fab, text_contains="page-lib-", state="*")  # указать стэйт
    # dp.register_callback_query_handler(callbacks_num_finish_fab, text_contains="station-call-", state="*")  # указать стэйт
    dp.register_message_handler(get_sp_and_fp_user_call, text='Последнее расписание', state="*")
    dp.register_message_handler(station_fsm_set, text='Выбор направления', state="*")
    # dp.register_callback_query_handler(station_fsm_question_start_place, text_contains="start", state=FSMSelectStation.start_place_question)
    dp.register_callback_query_handler(station_fsm_question_start_place, text_contains="station-call-", state=FSMSelectStation.start_place_question)
    dp.register_message_handler(station_fsm_question_finish_place, state=FSMSelectStation.start_place_check_answer)
    dp.register_callback_query_handler(station_fsm_check_answer_finish_place, text_contains="id", state=FSMSelectStation.finish_place_question)
