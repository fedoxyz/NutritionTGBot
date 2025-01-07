from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def confirm_cancel_kb():
    """Generate a confirmation and cancellation keyboard."""
    return ReplyKeyboardMarkup(
        [["🔙 Назад"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def product_overview_kb(product_id: int) -> InlineKeyboardMarkup:
    # Define callback data for each button
    keyboard = [
      #  [
      #      InlineKeyboardButton("✏️ Изменить название", callback_data=f"edit_name#{product_id}"),
      #      InlineKeyboardButton("🔢 Изменить количество", callback_data=f"edit_quantity#{product_id}"),
      #  ],
        [
            InlineKeyboardButton("🗑️ Удалить продукт", callback_data=f"remove_product#{product_id}"),
            InlineKeyboardButton("🏷️ Изменить категорию", callback_data=f"edit_category#{product_id}"),
            
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def categories_kb(categories: list) -> InlineKeyboardMarkup:
    keyboard = []
    # Store categories in context to reference them later
    for idx, category in enumerate(categories):
        keyboard.append([
            InlineKeyboardButton(
                text=category,  # Show full category name
                callback_data=f"set_category#{idx}"  # Use index in callback
            )
        ])
    return InlineKeyboardMarkup(keyboard)

