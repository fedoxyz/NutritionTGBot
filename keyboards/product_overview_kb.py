from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def confirm_cancel_kb():
    """Generate a confirmation and cancellation keyboard."""
    return ReplyKeyboardMarkup(
        [["💾 Сохранить", "🔙 Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
def product_overview_kb(product_id: int) -> InlineKeyboardMarkup:
    # Define callback data for each button
    keyboard = [
        [
            InlineKeyboardButton("✏️ Изменить название", callback_data=f"edit_name#{product_id}"),
            InlineKeyboardButton("🔢 Изменить количество", callback_data=f"edit_quantity#{product_id}"),
        ],
        [
            InlineKeyboardButton("🗑️ Удалить продукт", callback_data=f"remove_product#{product_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

