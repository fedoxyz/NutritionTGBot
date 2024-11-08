from telegram import KeyboardButton, ReplyKeyboardMarkup

def details_kb():
    keyboard = [
        [KeyboardButton("Подробнее"), KeyboardButton("Динамика ИЗП")],
        [KeyboardButton("Главное меню")],

    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

