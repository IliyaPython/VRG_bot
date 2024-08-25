#! python.exe
# Импортируем стандартные библиотеки
import json, time, base64, requests, asyncio, threading, random as rdm, os

# Импорты сторонних библиотек
from aiogram import types, Dispatcher, Bot, filters as fil, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import SendMessage
from aiogram.fsm.context import FSMContext
from aiogram import flags

# Импорт собсвтенных библиотек
import GenerModels as Models
from classes import *
import DataBase as db
from bot_commands.DnD_commands import *
from bot_commands import *
import utils


symbols = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
sym = lambda: rdm.choice(symbols)

key = os.environ["BOT TOKEN"]
conversation_history = {}

bot = Bot(
    token=key, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)  # Мы инициализируем бота с ключом key, и устанавливаем некоторые свойства по умолчанию, здесь
dsp = Dispatcher()

print(Models.Kandinsky.AUTH_HEADERS)

user_id = ""
last_message = ""
rooms = {}
RP_games = {
    "choiced": "",
    "D&D": {
        "Description": "Фэнтези, Подземелья и драконы, сказочные персонажи, приключения и бои.",
        "SystemDescription": "Ты - ведущий игры Dungeons & Dragons. Ты увлекательно и таинственно рассказываешь истории, выбираешь необычные пути развития сюжета."
        "Обращайся к команде. Но не говори лишнего, про командную работу и слаженность. Пиши не более 70 слов.",
    },
    "a": 1,
}
history = []
dsp.message.register(get_nickname, F.text, fsm_states[0])
dsp.message.register(get_class, F.text, fsm_states[1])
dsp.message.register(get_race, F.text, fsm_states[2])


# dsp.message.register(get_race, F.text, fsm_states[2], flags={"users": users})
dsp.message.register(send_instruction, fil.Command(commands=["help", "h"]))
@dsp.message(fil.Command(commands=["start", "s"]))
async def bot_message(message):
    global user_id
    user_id = str(message.chat.id)
    await db.manager.add_user(user_id)
    print(user_id)
    DnD = types.InlineKeyboardButton(
        text="🐲 Drag & Dung ⚔", callback_data="D&D"
    )
    soon = types.InlineKeyboardButton(text="Скоро.", callback_data="soon")
    # Создаем объект инлайн-клавиатуры
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[DnD, soon]])
    print("\n", markup, "\n")
    await message.answer(
        text="Я бот для командных настольных игр. Но со мной они станут в разы интереснее!\nЧтобы ознакомиться с правилами введите `/help` или `/h`.\nЧтобы войти в меню игр введите `/menu`",
        reply_markup=markup,
    )


#    bot.send_message(message.chat.id, "Я бот для командных настольных игр. Но со мной они станут в разы интереснее!\nЧтобы ознакомиться с правилами введите <code>/help</code> или <code>/h</code>.\nЧтобы войти в меню игр введите <code>/menu</code>", parse_mode='html', reply_markup=markup)
dsp.message.register(exiting, fil.Command(commands=["exit", "ex"]))


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'D&D' или "Скоро."
@dsp.callback_query(F.data.in_(["D&D", "Скоро."]))
async def processing_call(callback: types.CallbackQuery, state: FSMContext):
    print("Я тут, но другой босс!")
    if callback.data == "D&D":
        print("D&D")
        print(state.__dict__['storage'].__dict__)
        await Character.register(dsp=dsp,
                        user_id=callback.from_user.id,
                        fsm_for_callback=state)
        #? Одна из ошибок возникала в строке 86, из-за того, что в user_id передается число, в последствии (register -> get_characters_by_ID ->
        #?   -> if ID in database.keys()), а ключи базы данных = строки. Следовательно, раз int != str, то оно не найдет юзера
        determine_DnD(callback.from_user.id)
    elif callback.data == "soon":
        print("В разработке")
        await callback.answer()

def determine_DnD(user):
    global history
    history = [
        Models.Master.SystemMessage(content=RP_games["D&D"]["SystemDescription"])
    ]
    # Импорт файлов для работы с ботом
    from srcs import dnd
    @dsp.message(fil.Command(commands=["menu", "m", "M", "Menu"]))
    async def join_to_menu(message: types.Message):
        print("УРАА")
        global user_id
        user_id = message.chat.id
        markup = await utils.make_inlinekeyboard(["Присоединиться к комнате", "Создать комнату"],
                                           ["joinRoom", "createRoom"])
        await message.answer(  # В данном методе не нужно указывать ID, так как он работает следующим образом: метод .answer()
            # принимает параметр self (= message), а затем вызывает функцию SendMessage(self.chat.id), что = message.chat.id
            text="Вы зашли в меню. Вы можете <b>создать свою комнату</b> или <b>присоединиться к комнате.</b>",
            reply_markup=markup,
        )
        global last_message
        last_message = message

    # Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
    # с data 'D&D' или "Скоро."
    @dsp.callback_query(F.data.in_(["joinRoom", "createRoom"]))
    async def processing_callback(callback: types.CallbackQuery):
        print("я тут босс!")
        if callback.data == "joinRoom":
            callback.message.answer(
                text="Введите секретный ID для подключения (Добавив Code).\nНапример, Code: yyyyyyy"
            )
        elif callback.data == "createRoom":
            Id = eval(
                ("sym()+ " * 9)[:-2]
            )  # Это равнозначно вызову sym() 9 раз. В результате получаем строку 'sym()+ g...+ sym() +', поэтому берем всё, коме последнего знака ([:-2])
            await create_room(callback.message, Id)

    global processing_call
    # processing_call  # Удаляем первоначальную функцию "Обработка данных", чтобы избежать неполадок в будущем и чтобы в будущем она не вызывалась

    async def join_to_room(user_id, Id):
        global rooms
        users = (await db.manager.read_database("users")
                 ).keys()
        all_players = ", ".join(
            list(
                map(
                    lambda x: str(x)[1:-1], [rooms[x]["players"] for x in rooms]
                )
            )
        ).split(", ")
        print(all_players)
        if str(user_id) not in all_players:
            user = users[str(user_id)]
            rooms[Id]["players"].append(user)
        else:  # Иначе | =, если игрок состоит в команде
            if rooms[Id]["Status"] == True:  # Если игра началась, то
                pass  # игнорируем, чтобы создать видимость, что функция больше не доступна
            else:  # иначе | если игра не началась
                bot.send_message(
                    chat_id=user_id,
                    text="Вы уже состоите в комнате.",
                    parse_mode="html",
                )
        print("Ты вошел в комнату!", Id)

    async def create_room(message: types.Message, Id: str):
        global rooms
        users = (await db.manager.read_database("users")
                 ).keys()
        all_players = ", ".join(
            list(
                map(
                    lambda x: str(x)[1:-1], [rooms[x]["players"] for x in rooms]
                )
            )
        ).split(", ")
        if str(message.chat.id) not in all_players:
            user = [user for user in users if user == str(message.chat.id)][0]  
            # Здесь, нам необходим такой синтаксис по причине: приминить цикл for и if в одной строке можно
            # только заключив их в []. Они создадут список с юзерами.id == this_id, а такой элемент может быть всего один, значит, и элементов с списке 1
            await message.answer(text=f"Вот ваш ID для комнаты: `{Id}`")
            rooms[Id] = {
                "players": [user],  # Список пользователей
                "owner": user,  # Создатель комнаты
                "Game": "D&D",  # Выбранная игра
                "Status": False,  # Статус игры: началась - True, иначе - False
                "Cur Step": "Next",  # Текущий шаг. Нужен "для баланса вселенной" и для того, чтобы игроки не совершали действия в неподходящие моменты.
                "banned": [],  # Список забаненных пользователей
            }
            print("Ты создал комнату!", rooms)
            print(rooms)
        else:  # Иначе | =, если игрок состоит в команде
            if (
                Id in rooms and rooms[Id]["Status"] == True
            ):  # Если игра началась и id комнаты уже существует (->, не новый), то
                pass  # игнорируем, чтобы создать видимость, что функция больше не доступна
            else:  # иначе | если игра не началась
                bot.send_message(
                    chat_id=user_id,
                    text="Вы уже состоите в комнате.",
                    parse_mode="html",
                )

    @dsp.message(fil.Command(commands=["game", "g"]))
    async def start_game(message: types.Message):
        for Id in rooms:
            print("A")
            if (
                str(message.chat.id) == rooms[Id]["owner"] 
            ):  # Проверяем, является ли владельцем комнаты человек, который написал эту команду
                # history.append(master.HumanMessage("Игра началась! Мы отправляемся в долгое путешествие, а ты будешь нас сопровождать!"
                #                                   " В начале квеста должна быть подготовка и введение, например, чаепитие в баре. Придумай креативное начало истории, чтобы игрокам"
                #                                  " захотелось играть, будь креативен и не повторяйся!"))
                if len(rooms[Id]["players"]) > 0:
                    history.append(
                            Models.Master.HumanMessage(
                                "Что мы будем делать дальше и куда идти? Расскажи подробно и увлекающее. Придумай интересный квест. Обращайся непосредственно к команде на 'вы'. Но"
                                " не говори про командную работу. Ты должен лишь придумывать"
                            )
                        )
                    from_bot = Models.Master.chat.invoke(history)
                    await message.answer(from_bot.content)
                    rooms[Id]["Status"] = True
                    for user in rooms[Id]["players"]:
                        # Удаляем каждое сообщение
                        for m in history:
                            print(m)
                            # bot.delete_message(user, m.message_id)
                        await bot.send_message(
                            int(user),
                            text="Вы начали игру! Надеюсь, вы знакомы с правилами.",
                        )
                    break
                else:
                    await bot.send_message(
                        message.chat.id,
                        text="Вы не можете начать игру, так как вы один!",
                    )
                    break

    @dsp.message()
    async def general_chat(message: types.Message):
        users = (await db.manager.read_database("users")
                 )
        user = [user for user in users.keys() if user == str(message.chat.id)][0]
        if message.text.startswith("Code: "):
            print("Ура! Победа")
            await join_to_room(user_id=user, Id=message.text[6:])
        from_bot = ""
        for room in rooms:
            room = rooms[room]
            if user in room["players"]:  # Если игрок в этой комнате
                if room["Status"] == True:  # и если игра началась,
                    # то можно проверять команды ниже
                    if (
                        message.text.startswith("Result:")
                        and user == room["owner"]
                        and room["Cur Step"] == "Result"
                    ):
                        history.append(Models.Master.HumanMessage(message.text))
                        # history.append(master.HumanMessage(content=message.text[8:]))
                        room["Cur Step"] = "Next"
                    elif (
                        message.text.startswith("Next:")
                        and user == room["owner"]
                        and room["Cur Step"] == "Next"
                    ):
                        from_user = message.text.removeprefix("Next:")
                        history.append(Models.Master.HumanMessage(
                            content=from_user  
                        ))
                        print(history)
                        print(f"\n {from_bot} \n")
                        from_bot = Models.Master.chat.invoke(history)
                        history.append(from_bot)
                        room["Cur Step"] = "Result"
                        from_bot = from_bot.content
                        prompt = await utils.generate_prompt_for_image(history=history, prompt="Base")
                        print(prompt)
                        image = await Models.generate_image(Models.Kandinsky, prompt, "temp")
                        await message.answer_photo(photo=image, caption=from_bot)
                for player in room["players"]:
                    if (
                        player != message.chat.id
                    ):  # Так как Player - это объект класса Player..., у него есть свойство id, по которому мы проверяем пользователя
                        print(user, " - ", users)
                        message_in_game = (
                            f"_{users[user]["Current Character"].get("nickname")}_   --  "
                            f"*{users[user]["Current Character"].get("HeroClass")[1]}-{users[user]["Current Character"].get("race")[1]}*"
                            f"\n{message.text}"
                        )

                        await bot.send_message(
                            chat_id=player, text=message_in_game
                        )
                        # await bot.send_photo(chat_id=player, photo=photo, caption=from_bot)
                    print(message.message_id)

                print(history)


print("All working")
dsp.run_polling(bot)
