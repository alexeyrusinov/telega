from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import ADMIN_ID
from func.date_and_time import get_data_time_ekb
from func.pars_bus import get_json_bus_data
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


myMenu = InlineKeyboardMarkup(row_width=2)
btnRandom = InlineKeyboardButton(text="узнать число", callback_data="btnRandom")
btnUrl = InlineKeyboardButton(text="Перейти на канал", url="https://t.me/python2day")
btnShare = InlineKeyboardButton(text="Поделиться", switch_inline_query="Лучший бот в мире!")

btnSub = InlineKeyboardButton(text="Купить подписку", callback_data="buySub")
btnVip = InlineKeyboardButton(text="Купить VIP", callback_data="buyVip")

myMenu.insert(btnRandom)
myMenu.insert(btnUrl)
myMenu.insert(btnShare)
myMenu.insert(btnSub)
myMenu.insert(btnVip)


btnMain = KeyboardButton("Главное меню")

################
btnStation = KeyboardButton("Выбор направления")
btnBtc = KeyboardButton("BTC/USDT")
btnUsd = KeyboardButton("USDT/RUB")
btn_ex_rate = KeyboardButton("Exchange rate")
btnLast = KeyboardButton("Последнее расписание")
btnOther = KeyboardButton("Другое")
btn_all_db = KeyboardButton("alldb")
btn_send = KeyboardButton("send")
btn_del_users = KeyboardButton("del")


def user_and_admin_menu(user_id):
    if user_id == ADMIN_ID:
        admin_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStation, btnLast).add(btn_ex_rate, btnOther)\
            .add(btn_del_users, btn_all_db, btn_send)
        return admin_menu
    else:
        user_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStation, btnLast).add(btnBtc, btnUsd, btnOther)
        return user_menu

##############


# other menu
btnTime = KeyboardButton("Текущее время и дата")
btnRandint = KeyboardButton("inlineButtons")
btnSchedule = KeyboardButton("Расписание на ближайшие дни")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSchedule).add(btnTime, btnRandint, btnMain)

# bus_answer_menu
btn_answer1 = KeyboardButton("все автобусы")
btn_answer2 = KeyboardButton("отправленные")
btn_answer3 = KeyboardButton("отмененные")
btn_answer4 = KeyboardButton("ближайшие")
btn_cancel = KeyboardButton("отмена")
bus_answer_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_answer4)\
                                                           .add(btn_answer1, btn_answer2)\
                                                           .add(btn_answer3, btn_cancel)

# check menu
btn_yes = KeyboardButton("верно")
check_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_yes, btn_cancel)

# cancel menu
cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)


# generate inline menu date schedule
def generate_keyboard(data):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for k, v in data.items():
        keyboard.insert(InlineKeyboardButton(text=v, callback_data=k))
    return keyboard


def generation_date_schedule(start_place, finish_place):
    mydict = {}
    for i in range(15):
        req = get_json_bus_data(start_place, finish_place, i)
        if req and len(req['rasp']) > 1:
            mydict.update({f"{i} - day": get_data_time_ekb(i).strftime('%d-%m-%Y')})
        else:
            break
    result = generate_keyboard(mydict)
    logger.info(f"generation_date_schedule - {len(mydict)} items")
    return result

# ------------------------------


# generate inline menu stations
def generate_keyboard_station(data, text_contains, row_wight=2):
    keyboard = InlineKeyboardMarkup(row_width=row_wight)
    for k, v in data.items():
        values_plus_id = str(v + f" {text_contains}")
        keyboard.insert(InlineKeyboardButton(text=k, callback_data=values_plus_id))
    return keyboard
