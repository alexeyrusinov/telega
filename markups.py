from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

# admin menu
btnBtc = KeyboardButton("Курс биткоина")
btnInfo = KeyboardButton("Расписание автобуса")
btnOther = KeyboardButton("Другое")
btn_all_db = KeyboardButton('all db')
adminMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnInfo).add(btnBtc, btnOther).add(btn_all_db)

# user menu
btnBtc = KeyboardButton("Курс биткоина")
btnInfo = KeyboardButton("Расписание автобуса")
btnOther = KeyboardButton("Другое")

userMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnInfo).add(btnBtc, btnOther)

# other menu
btnTime = KeyboardButton("Текущее время и дата")
btnRandint = KeyboardButton("inlineButtons")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime,btnRandint, btnMain)

# bus_answer_menu
btn_answer1 = KeyboardButton("1")
btn_answer2 = KeyboardButton("2")
btn_answer3 = KeyboardButton("3")
btn_answer4 = KeyboardButton("4")
bus_answer_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_answer1, btn_answer2, btn_answer3).add(btn_answer4)