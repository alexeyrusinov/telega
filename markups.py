from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

myMenu = InlineKeyboardMarkup(row_width=2)
btnRandom = InlineKeyboardButton(text="узнать число", callback_data="btnRandom")
myMenu.insert(btnRandom)



btnMain = KeyboardButton("Главное меню")


# main menu
btnBtc = KeyboardButton("Курс биткоина")
btnInfo = KeyboardButton("Расписание автобуса")
btnOther = KeyboardButton("Другое")
btn_all_db = KeyboardButton('all db')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo).add(btnBtc, btnOther).add(btn_all_db)

# other menu
btnTime = KeyboardButton("Текущее время и дата")
btnRandint = KeyboardButton("Случайное число")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime,btnRandint, btnMain)