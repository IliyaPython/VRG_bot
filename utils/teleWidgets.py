from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                           ReplyKeyboardMarkup, KeyboardButton
                           )


async def make_inlinekeyboard(
    resources: list[str], data: list[str], limit_per_string: int = 2
) -> InlineKeyboardMarkup:
    """
    Создает инлайн клавиатуру с {resources}, по {limit_per_string} на строку.

    Args:
        resources (List[str]): Список объектов, которые нужно добавить в клавиатуру.
        data (List[str]): Список callback_data для каждого объекта resources
        limit_per_string (int): Ограничение по кнопкам на одну строчку клавиатуры. Максимум = len(resources).
    Returns:
        InlineKeyboardMarkup: Созданная инлайн клваиутуру.
    """
    if not 0 < limit_per_string <= 100:
        raise Exception(
            "Limit error: Пределы по ограничению строки; значение limit_per_string не может превышать 100 или быть меньше 0."
        )
    if len(data) < len(
        resources
    ):  # Если количество callback_data не равно количеству кнопок или меньше. Если кнопок больше, программа в расчёт их не берёт
        raise Exception(
            "количество данных из data не указано для каждого объекта из resources. Добавьте дополнительные данные в data."
        )
    if resources:
        # Подготавливаем переменные для работы ниже
        keyboard = []
        row = []
        limit_per_string = (
            len(resources)
            if limit_per_string > len(resources)
            else limit_per_string
        )
        # Если ограничение на строку больше чем количество значений, то округляем
        # Иначе, оставляем как было
        for index, button in enumerate(resources, 0):
            temp = InlineKeyboardButton(text=button, callback_data=data[index])
            row.append(temp)

            if (
                len(row) >= limit_per_string
            ):  # Если количество обьектов в строке достигло максимума
                keyboard.append(row)
                row = []

        return InlineKeyboardMarkup(
            inline_keyboard=keyboard  # В keyboard у нас хранится список из строк по x кнопок
        )  # Возвращение объекта типа InlineKeyboardMarkup


async def format_button(obj: str, united_text: bool = False):
    return obj

async def make_replyKeyboard(items: list[str], limit_per_string: int = 1) -> ReplyKeyboardMarkup:  
    limit_per_string = (
        len(items)
        if limit_per_string > len(items) # Если ограничение на строку больше чем количество значений, то округляем
        else limit_per_string # Иначе, оставляем как было
    )
    
    keyboard = []
    row = []
    for button in items:
            temp = KeyboardButton(text=button)
            row.append(temp)

            if (len(row) >= limit_per_string
                ):  # Если количество обьектов в строке достигло максимума
                keyboard.append(row)
                row = []
    print(keyboard)
    return ReplyKeyboardMarkup(keyboard=keyboard)