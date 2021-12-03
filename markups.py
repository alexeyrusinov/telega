from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnMain = KeyboardButton("Главное меню")

# main menu
btnTime = KeyboardButton("Текущее время и дата")
btnOther = KeyboardButton("Другое")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime, btnOther)

# other menu
btnInfo = KeyboardButton("Информация")
btnMoney = KeyboardButton("Курс биткоина")
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMoney, btnMain)