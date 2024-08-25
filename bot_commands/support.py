import os, json

from aiogram import Dispatcher, filters
from aiogram.types import Message
from aiogram.enums import ParseMode

from utils.teleWidgets import make_inlinekeyboard, format_button


async def greet_user(message: Message) -> None:
    message.answer(
        text="""Я бот для командных настольных игр. Но со мной они станут в разы интереснее!
                    Чтобы ознакомиться с правилами введите `/help` или `/h`.
                    Чтобы войти в меню игр введите `/menu`"""
    )
    await add_new_user(message.chat.id)


async def add_new_user(ID: int) -> None:
    with open(os.path.relpath("users.json"), "r") as db:
        data = json.load(db)
        data[ID] = {"characters": []}
    with open(os.path.relpath("users.json"), "w") as db:
        json.dump(data, db)


async def exiting(message: Message) -> None:
    keyboard = await make_inlinekeyboard(
        ["Да, уверен.", "Нет, не уверен"],
        ["Exit_user_allow", "Exit_user_cancel"],
    )
    print(keyboard)
    await message.reply(
        text="_Вы уверены, что хотите выйти из бота?_\nЭто приведёт к тому ...",
        reply_markup=keyboard,
    )


async def send_instruction(message: Message):
    print("AM HERE")
    print(message.text)
    text = message.text.split()
    if len(text) != 2:
        print("!")
        await message.reply("Пожалуйста, укажите /help в правильном запросе или напишите создателю. Например, `/help DnD`")
    else:
        print("2")
        game = text[-1].lower()
        path_to_instruction = f"srcs/{game}/instruction.txt"
        with open(path_to_instruction, "r", encoding="utf-8") as inst:
            # print(inst.read())
            await message.reply(inst.read(), parse_mode=ParseMode.HTML) # TODO: КТо такой 5780160180, игравший в моего бота?


def register(dsp: Dispatcher):
    dsp.message.register(send_instruction, filters.Command(commands=["help", "h"]))
    dsp.message.register(exiting, filters.Command(commands=["exit", "ex"]))