from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import ADMIN_ID

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

inlineMenu = InlineKeyboardMarkup(row_width=1)
btnAllBuses = InlineKeyboardButton(text="Все автобусы", callback_data="all_buses")
btnDispatchedBuses = InlineKeyboardButton(text="Отправленные", callback_data="dispatched_buses")
btnCanceledBuses = InlineKeyboardButton(text='Отмененные', callback_data="buses_canceled")
btnGetBuses = InlineKeyboardButton(text="Ближайшие", callback_data="bus_schedule")

inlineMenu.insert(btnAllBuses)
inlineMenu.insert(btnDispatchedBuses)
inlineMenu.insert(btnCanceledBuses)
inlineMenu.insert(btnGetBuses)

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
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime,btnRandint, btnMain)

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