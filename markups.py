from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnMain = KeyboardButton("Главное меню")

# main menu

btnBtc = KeyboardButton("Курс биткоина")
btnInfo = KeyboardButton("Расписание автобуса")
btnOther = KeyboardButton("Другое")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo).add(btnBtc, btnOther)

# other menu
btnTime = KeyboardButton("Текущее время и дата")

otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime, btnMain)