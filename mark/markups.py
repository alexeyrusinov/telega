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


def user_and_admin_menu(user_id):
    if user_id == ADMIN_ID:
        # admin menu
        btnBtc = KeyboardButton("Курс биткоина")
        btnInfo = KeyboardButton("Расписание автобуса")
        btnOther = KeyboardButton("Другое")
        btn_all_db = KeyboardButton("alldb")
        btn_send = KeyboardButton("send")
        btn_del_users = KeyboardButton("del")
        adminMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo).add(btnBtc, btnOther).add(btn_del_users, btn_all_db, btn_send)
        return adminMenu
    else:
        # user menu
        btnBtc = KeyboardButton("Курс биткоина")
        btnInfo = KeyboardButton("Расписание автобуса")
        btnOther = KeyboardButton("Другое")
        userMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo).add(btnBtc, btnOther)
        return userMenu

##############


# other menu
btnTime = KeyboardButton("Текущее время и дата")
btnRandint = KeyboardButton("inlineButtons")
btnSchedule = KeyboardButton("inline schedule")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSchedule, btnRandint).add(btnTime, btnMain)

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


def generation_date_schedule():
    mydict = {}
    for i in range(15):
        req = get_json_bus_data(i)
        if req and len(req['rasp']) > 1:
            mydict.update({f"{i} - day": get_data_time_ekb(i).strftime('%d-%m-%Y')})
        else:
            break
    result = generate_keyboard(mydict)
    logger.info(f"generation_date_schedule - {len(mydict)} items")
    return result
