import random as rn

from aiogram.types import FSInputFile, Message


class Dyce:
    async def dice6():
        number = rn.randint(1, 6)
        photo = FSInputFile(f"src/imgs/dices/{number}D6.png")
        return (number, photo)

    async def dice20():
        number = rn.randint(1, 20)
        photo = FSInputFile(f"src/imgs/dices/{number}D20.png")
        return (number, photo)
