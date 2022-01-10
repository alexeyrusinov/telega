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
# myMenu.insert(btnSomething)
myMenu.insert(btnSub)
myMenu.insert(btnVip)

inlineMenu = InlineKeyboardMarkup(row_width=1)
btnAllBuses = InlineKeyboardButton(text="Все автобусы", callback_data="all_buses")
btnDispatchedBuses = InlineKeyboardButton(text="Отправленные автобусы", callback_data="dispatched_buses")
btnGetBuses = InlineKeyboardButton(text="Расписание", callback_data="bus_schedule")

inlineMenu.insert(btnAllBuses)
inlineMenu.insert(btnDispatchedBuses)
inlineMenu.insert(btnGetBuses)



btnMain = KeyboardButton("Главное меню")


# main menu
btnBtc = KeyboardButton("Курс биткоина")
btnInfo = KeyboardButton("Расписание автобуса")
btnOther = KeyboardButton("Другое")
btn_all_db = KeyboardButton('all db')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo).add(btnBtc, btnOther).add(btn_all_db)

# other menu
btnTime = KeyboardButton("Текущее время и дата")
btnRandint = KeyboardButton("inlineButtons")
# btnInlineTest = KeyboardButton()
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime,btnRandint, btnMain)