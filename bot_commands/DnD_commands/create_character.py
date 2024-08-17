from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State
from aiogram.types import Message
from aiogram.dispatcher import flags
from aiogram.dispatcher.event.telegram import TelegramEventObserver

from classes import DnDPlayer
from classes.DND_Staff.ClassResource import CLASSES
from classes.DND_Staff.RaceResource import RACES

fsm_states = [
    State("Nickname"),
    State("Class"),
    State("Race"),
]

async def get_nickname(message: Message,
                       state: FSMContext):
    print(state)
    print(message.text)
    await state.update_data(nickname=message.text)
    await message.answer(text="Отлично! Теперь введите класс игрока одним словом по-английски.")
    await state.set_state(fsm_states[1])
    print("\n\n", state,"-", fsm_states[1])

async def get_class(message: Message,
                       state: FSMContext):
    print(message, "\n\n", state, "-", fsm_states[2])
    gClass = message.text
    print(message.text)
    if not gClass or gClass not in CLASSES:
        await message.reply('Извините, такого класса нет. Если вы не знаете доступных классов, вы можете вызвать `/help`')

        return # завершаем программу, пропуская код ниже
    await state.update_data(hClass=gClass)
    await message.answer(text="Прекрасный выбор! Теперь расу")
    await state.set_state(fsm_states[2])

async def get_raace(handler, event, data):
    flags_data = flags.extract_flags(data)
    print(f"{flags_data = }")

    return await handler(event, data)

async def get_race(message: Message,
                   state: FSMContext): # Мы не указывем здесь параметров, так как эта функция сама соберёт их в 3 нижних строках.
    users = fsm_states[3]
    print(users)
    print(users)
    # users = flags.get_flag(data, "users")
    race = message.text.title()
    print(race)
    if not race or race not in RACES:
        await message.reply('Извините, такой расы нет. Если вы не знаете доступных рас, вы можете вызвать `/help`')
        return # завершаем программу, пропуская код ниже
    await state.update_data(race=race)

    data = await state.get_data()
    nickname, hClass, hRace = data.get("nickname"), data.get("hClass"), data.get("race")
    hero = DnDPlayer(message.from_user.id, nickname, hClass, hRace)
    users[message.from_user.id]["characters"].append(hero)
    print(hero)
    await message.answer(text="Отлично! Ваш герой создан")
    await state.clear()