from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import math
import sqlite3 as sq
import my_db
from func.bus_func import get_schedule_with_type
from func.work_on_file import get_station, get_name_station
from mark import markups as nav
from create_bot import bot
from mark.markups import generation_date_schedule

user_data = {}


def get_keyboard_fab_sp(name_table: str, page=1, elem_on_page=6):
    all_items = 24
    max_page = math.ceil(all_items / elem_on_page)
    skip = (page - 1) * elem_on_page
    with sq.connect("files/station.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM %s LIMIT %s OFFSET %s" % (name_table, elem_on_page, skip))
        items = cur.fetchall()
        cur.close()
    result_stations = []
    for i in items:
        result_stations.append(types.InlineKeyboardButton(text=i[0], callback_data=f"start-call-{i[1]}"))

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
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data=f"page-lib-{page - 1}"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}/{max_page}", callback_data="None"))
        service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
    else:
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data=f"page-lib-{page - 1}"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}/{max_page}", callback_data="None"))
        if page < max_page:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data=f"page-lib-{page + 1}"))
        else:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
    keyboard.add(*service_buttons)
    return keyboard


def get_keyboard_fab_fp(name_table: str, value_station: str, page=1, elem_on_page=7):
    default_element_on_page = 6
    skip = (page - 1) * default_element_on_page
    word = f"'%{value_station}%'"

    with sq.connect("files/station.db") as con:
        cur = con.cursor()
        cur.execute("SELECT name_station_fp, station_call_fp "
                    "FROM %s "
                    "WHERE name_station_lower_fp LIKE %s "
                    "LIMIT %s OFFSET %s" % (name_table, word, elem_on_page, skip))
        items = cur.fetchall()
        flag = None
        if len(items) > default_element_on_page:
            flag = True
            items.pop(-1)
        cur.close()
    result_stations = []
    for i in items:
        result_stations.append(types.InlineKeyboardButton(text=i[0], callback_data=f"station-call-{i[1]}"))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*result_stations)

    service_buttons = list()
    keyboard.row_width = 3
    if page == 1:
        # service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data="None"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}", callback_data="None"))
        if len(result_stations) < default_element_on_page:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
        else:
            service_buttons.append(types.InlineKeyboardButton(text="->", callback_data=f"page-fp-2"))
    elif flag is None:
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data=f"page-fp-{page - 1}"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}", callback_data="None"))
        # service_buttons.append(types.InlineKeyboardButton(text="->", callback_data="None"))
    elif flag:
        service_buttons.append(types.InlineKeyboardButton(text="<-", callback_data=f"page-fp-{page - 1}"))
        service_buttons.append(types.InlineKeyboardButton(text=f"{page}", callback_data="None"))
        service_buttons.append(types.InlineKeyboardButton(text="->", callback_data=f"page-fp-{page + 1}"))
    keyboard.add(*service_buttons)
    return keyboard


async def update_keyboard_fab_sp(message: types.Message, page: int, name_table, ):
    with suppress(MessageNotModified):
        await message.edit_reply_markup(reply_markup=get_keyboard_fab_sp(name_table=name_table, page=page))


async def update_keyboard_fab_fp(message: types.Message, page: int, value_station, name_table, ):
    with suppress(MessageNotModified):
        await message.edit_reply_markup(
            reply_markup=get_keyboard_fab_fp(name_table=name_table, value_station=value_station, page=page))


class FSMSelectStation(StatesGroup):
    start_place_question = State()
    start_place_check_answer = State()
    finish_place_question = State()


next_schedule = {}


async def station_fsm_set(message: types.Message, flag_next_schedule=False):
    await my_db.sql_add_user(message)
    next_schedule[message.from_user.id] = flag_next_schedule
    await FSMSelectStation.start_place_question.set()
    await message.reply("Откуда: ", reply_markup=get_keyboard_fab_sp(name_table="start_place"))
    await message.answer("Выбирай..", reply_markup=nav.cancel_menu)


# @dp.callback_query_handler(text_contains="page-lib-")
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
async def callbacks_num_change_fab_sp(call: types.CallbackQuery):
    page = int(call.data[-1])
    await update_keyboard_fab_sp(call.message, page=page, name_table="start_place")
    await call.answer()


async def callbacks_num_change_fab_fp(call: types.CallbackQuery):
    page = call.data.split('-')
    await update_keyboard_fab_fp(call.message, page=int(page[-1]), name_table="finish_place",
                                 value_station=user_data[call.from_user.id])
    await call.answer()


async def get_sp_and_fp_user_call(message: types.Message):
    await my_db.sql_add_user(message)
    with sq.connect("files/users.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT start_place_call, finish_place_call, type_schedule  FROM users WHERE user_id = ?""",
                    (message.from_user.id,))
        result = cur.fetchall()
        cur.close()
        if result[0][0] == str(None) and result[0][1] == str(None):
            await station_fsm_set(message)
        else:
            await message.answer(get_schedule_with_type(result[0][0], result[0][1], days=0, type_schedule=result[0][2]),
                                 parse_mode="Markdown")


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
    user_data[message.from_user.id] = message.text.lower()
    if len(dict_with_result_station) == 0:
        await message.answer("Попробуй ещё..\nКуда: (например: Екатеринбург) ", reply_markup=nav.cancel_menu)
        await FSMSelectStation.start_place_check_answer.set()
    else:
        await message.answer("Какую из:", reply_markup=get_keyboard_fab_fp(name_table="finish_place",
                                                                           value_station=user_data[message.from_user.id]))
        await FSMSelectStation.next()


async def station_fsm_check_answer_finish_place(call: types.CallbackQuery, state: FSMContext):
    call_user_station = []
    user_answer = call.data.split('-')
    for word in user_answer:
        if word.isnumeric():
            call_user_station.append(int(word))
    async with state.proxy() as data:
        data["finish_place_user_call"] = call_user_station[-1]
        start_place = data["start_place"]
        finish_place = get_name_station('files/704.json', call_user_station[0])
        start_call = data["start_place_user_call"]
        finish_call = data["finish_place_user_call"]
        data_user = (call.from_user.id, call.from_user.username, call.from_user.first_name)
        if next_schedule[call.from_user.id]:
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await bot.send_message(call.from_user.id, 'Выбирай..', reply_markup=nav.otherMenu)
            await bot.send_message(call.from_user.id, f"от *{start_place}* до *{finish_place}*",
                                   reply_markup=generation_date_schedule(start_place=start_call,
                                                                         finish_place=finish_call),
                                   parse_mode="Markdown")
            await call.answer()
            await state.finish()
        else:
            with sq.connect("files/users.db") as con:
                cur = con.cursor()
                cur.execute("""SELECT type_schedule  FROM users WHERE user_id = ?""",
                            (data_user[0],))
                items = cur.fetchone()
                print(items, 'items')
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await bot.send_message(call.from_user.id,
                                   f"{get_schedule_with_type(start_call, finish_call, days=0, type_schedule=items[0])}",
                                   reply_markup=nav.user_and_admin_menu(call.from_user.id), parse_mode="Markdown")

        await my_db.update_sp_and_fp_call(data_user, start_call, finish_call)
    await call.answer()
    await state.finish()


def register_handlers_bus_station(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_num_change_fab_sp, text_contains="page-lib-", state="*")
    dp.register_callback_query_handler(callbacks_num_change_fab_fp, text_contains="page-fp-", state="*")
    dp.register_message_handler(get_sp_and_fp_user_call, text='Последнее расписание', state="*")
    dp.register_message_handler(station_fsm_set, text='Выбор направления', state="*")
    dp.register_callback_query_handler(station_fsm_question_start_place, text_contains="start-call-",
                                       state=FSMSelectStation.start_place_question)
    dp.register_message_handler(station_fsm_question_finish_place, state=FSMSelectStation.start_place_check_answer)
    dp.register_callback_query_handler(station_fsm_check_answer_finish_place, text_contains="station-call-",
                                       state=FSMSelectStation.finish_place_question)
