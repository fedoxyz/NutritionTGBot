from telegram import KeyboardButton, ReplyKeyboardMarkup

def nutrition_kb():
    keyboard = [
        [KeyboardButton("Витамины"), KeyboardButton("Минералы")],
        [KeyboardButton("Аминокислоты"), KeyboardButton("Состав жиров")],
        [KeyboardButton("Состав углеводов"), KeyboardButton("Психоактивные вещества")],
        [KeyboardButton("Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
