import random as rn

from aiogram.types import Message, FSInputFile, InputMediaPhoto


async def roll_dice2(message: Message):
    number = rn.randint(1, 3)
    photo = FSInputFile(f"src/imgs/dices/{number}D2png")
    caption = f"И вот! Ваше число {number}."
    await message.answer_photo(photo, caption=caption)
