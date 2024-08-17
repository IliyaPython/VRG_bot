from aiogram.types import Message

async def greet_user(message: Message) -> None:
    message.answer(text="""Я бот для командных настольных игр. Но со мной они станут в разы интереснее!
                    Чтобы ознакомиться с правилами введите `/help` или `/h`.
                    Чтобы войти в меню игр введите `/menu`""")
    await add_new_user(message.chat.id)

async def add_new_user(ID: int) -> None:
    with open(os.path.relpath("users.json"), "r") as db:
        data = json.load(db)
        data[ID] = {
            "characters": []
        }
    with open(os.path.relpath("users.json"), "w") as db:
        json.dump(data, db)