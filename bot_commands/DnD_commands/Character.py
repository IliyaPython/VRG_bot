import numpy as np

from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.teleWidgets import make_inlinekeyboard
from DataBase.manager import get_characters_by_ID, replace_data_user, get_character_by_UID
from .create_character import fsm_states


async def choice_character(message: Message,
                           state: FSMContext): # Главная функция. Отвечает за первое сообщение о персонажах в игре
    user_id = message.chat.id
    # Проверяем, есть ли у пользователя уже созданные персонажи
    existing_characters = await get_characters_by_ID(user_id)

    if existing_characters:
        # Если у пользователя есть хотя бы один персонаж, предлагаем выбор
        keyboard = await make_inlinekeyboard(
            ["Выбрать персонажа", "Создать персонажа"],
            ["choice_char", "create_new_char"],
            2,
        )

        await message.reply(
            "У вас уже есть созданные персонажи. Что вы хотите сделать?",
            reply_markup=keyboard,
        )
    else:
        # Если у пользователя нет персонажей, создаем нового
        await create_new_character(user_id, message, state)


async def create_new_character(ID, message, state):
    await state.set_state(
            fsm_states[0]
        )  # Начинаем перовый шаг: ставим состояние "Выбирает ник", а далее по списку
    await message.answer("Кто ты, воин? Как мне звать тебя?")


async def proccesing_character_callback(callback: CallbackQuery, # Обрабатывает данные, полученые в результате выполнения choice_character
                                        state: FSMContext): #* state (Почему не Fsm?), а потому, что есть особенность:
                                        #*  наверняка, при "распаковке" аргументов, был параметр state (object at FSMContext). Вот он и передаётся, вот так:
                                        #* `state=(Some object at FSMContext)`. То есть, имя для таких объектов заранее придумано. Не получится указать
                                        #* аргумент (a="yes"), если в функции есть только параметры (b, c)
    user_id = callback.from_user.id
    fsm = state

    if callback.data == "create_new_char":
        await create_new_character(
            ID = user_id,
            message = callback.message,
            state = fsm
        )

    elif callback.data == "choice_char":
        characters = await get_characters_by_ID(user_id, returnNames = True)
        print(characters)
        characters = np.array(characters) # Создаём массив из элементов tuple: (id, nickname)
        print(characters)

        lenght = len(characters)

        keyboard = await make_inlinekeyboard(characters[:lenght, 1].tolist(), # Достаём из массива только ник, но для каждого персонажа
                                             characters[:lenght, 0].tolist(), # Достаём только ID объекта, но для всех персонажей
                                             1)
        
        await callback.message.answer("Хорошо. Выберите одного из своих персонажей ниже:",
                                reply_markup=keyboard)
        

async def handle_character(callback: CallbackQuery):
    """Собиратель персонажа. Реагирует на любое ID персонажа.
        ## Логика:
            1. Достаёт ID пользователя
            2. Достаёт персонажа, выбранного пользователем.
            3. Меняет текущего персонажа на выбранного персонажа
        ## Returns: None
    """
    user_id = callback.from_user.id
    try:
        char_to_play = await get_character_by_UID(user_id,
                                                  callback.data)
        print(char_to_play)
        await replace_data_user(user_id, "Current Character", char_to_play, None)
    except Exception as e:
        print(f"\nError occured: {e}\n")


async def register(dsp: Dispatcher,
             user_id: int,
             fsm_for_callback):
    print("YESS")
    dsp.message.register(choice_character, Command(commands=["chars", "characters"]))
    dsp.callback_query.register(proccesing_character_callback, F.data.in_(["choice_char", "create_new_char"]))
    characters = await get_characters_by_ID(user_id)
    print(characters)
    print(("243a4328-62aa-11ef-bdae-f835dd44745d" in characters))
    dsp.callback_query.register(handle_character, F.data.in_(characters))