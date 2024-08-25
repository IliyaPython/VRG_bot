from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State
from aiogram.types import Message
from aiogram.dispatcher import flags
from aiogram.dispatcher.event.telegram import TelegramEventObserver

from GenerModels.kandinsky import Kandinsky
from classes import DnDCharacter
from classes.DND_Staff.ClassResource import CLASSES
from classes.DND_Staff.RaceResource import RACES
import utils
import DataBase as db
import GenerModels as Models

fsm_states = [
    State("Nickname"),
    State("Class"),
    State("Race"),
]


async def get_nickname(message: Message, state: FSMContext):
    print(state)
    print(message.text)
    await state.update_data(nickname=message.text)
    keyboard = await utils.make_replyKeyboard(CLASSES.keys(), 1)
    await message.answer(
        text="Отлично! Теперь введите класс игрока одним словом по-английски.",
        reply_markup=keyboard
    )
    await state.set_state(fsm_states[1])
    print("\n\n", state, "-", fsm_states[1])


async def get_class(message: Message, state: FSMContext):
    print(message, "\n\n", state, "-", fsm_states[2])
    gClass = (
        message.text.lower()
    )  # Приводим к нижнему регистру текст сообщения для проверки в будущем
    print(gClass)

    isExists = False
    for CLASS in CLASSES:
        CLASS_temp = CLASSES[CLASS]
        if gClass in CLASS_temp:  # Если класс существует
            isExists = True
            gClass = CLASS
            break
    if not isExists:
        await message.reply(
            "Извините, такого класса нет. Если вы не знаете доступных классов, вы можете вызвать `/help`"
        )
        return  # завершаем программу, пропуская код ниже

    await state.update_data(hClass=gClass)
    keyboard = await utils.make_replyKeyboard(RACES.keys(), 1)
    await message.answer(text="Прекрасный выбор! Теперь расу", 
                         reply_markup=keyboard)
    await state.set_state(fsm_states[2])


async def get_race(message: Message, state: FSMContext):
    users = await db.manager.read_database("users")
    print(users)
    print(users)
    # users = flags.get_flag(data, "users")
    race = message.text.lower()
    print(race)

    isExists = False
    for RACE in RACES:
        print(RACE)
        RACE_temp = RACES[RACE]
        print(RACE_temp)
        if race in RACE_temp:  # Если раса существует
            print("OK")
            isExists = True
            race = RACE
            break
    if not isExists:
        await message.reply(
            "Извините, такой расы нет. Если вы не знаете доступных рас, вы можете вызвать `/help`"
        )
        return  # завершаем программу, пропуская код ниже

    await state.update_data(race=race)
    data = await state.get_data()
    nickname, hClass, hRace = (
        data.get("nickname"),
        data.get("hClass"),
        data.get("race"),
    )
    temp = DnDCharacter(message.from_user.id, nickname, hClass, hRace)
    try:
        char = temp.__metadata__
        print(char)
        user_id = str(message.from_user.id)
        print(user_id)
        users[user_id]["Characters"].append(char)
        await db.manager.replace_data_user(user_id, "Characters", users[user_id]["Characters"])
        await db.manager.replace_data_user(user_id, "Current Character", char)
        # TODO: Сделать оптимизацию для замены ключей в базе данных, то есть, чтобы в одной команде можно было вводить сразу несколько ключей

        prompt = await utils.generate_prompt_for_image(history=[], prompt= ("Сгенерируй промпт для Кандинского на английском. "
                f"Красочно опиши персонажа. Вот данные: Name {char["nickname"]}, Class {char["gClass"]}, race {char["race"]}. Кроме промпта ничего не пиши, только описание персонажа!"))
        photo = await Models.generate_image(Kandinsky, prompt, "temp_avatar")
    except KeyError:
        await message.reply(text="Во время создания персонажа произошла ошибка. Попробуйте заново написать боту: очистить чат и ввести `/s`")
    else:
        print(temp, " ---  ", char)
        await message.reply_photo(
            photo = photo,
            caption="""
                Вы успешно создали персонажа! Чтобы войти в меню введите команду `/menu` (Копировать).
                            """
        )
        await state.clear()
