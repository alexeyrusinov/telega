from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnMain = KeyboardButton("Главное меню")

# main menu

btnBtc = KeyboardButton("Курс биткоина")
btnOther = KeyboardButton("Другое")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnBtc, btnOther)

# other menu
btnInfo = KeyboardButton("Информация")
btnTime = KeyboardButton("Текущее время и дата")

otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnTime).add(btnMain)