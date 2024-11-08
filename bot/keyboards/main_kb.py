from telegram import KeyboardButton, ReplyKeyboardMarkup

def main_kb():
    keyboard = [
        [KeyboardButton("Баланс макронутриентов"), KeyboardButton("Индекс здорового питания")],
        [KeyboardButton("Категории продуктов"), KeyboardButton("Химсостав рациона")],
        [KeyboardButton("Разнообразие рациона"), KeyboardButton("Доля переработанных продуктов")],
        [KeyboardButton("Источники данных")],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
