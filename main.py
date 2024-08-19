#! python.exe
# Импортируем стандартные библиотеки
import json, time, base64, requests, asyncio, threading, random as rdm, os
# Импорты сторонних библиотек
from aiogram import (types, 
            Dispatcher, Bot,
            filters as fil, F)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import SendMessage
from aiogram.fsm.context import FSMContext
from aiogram import flags

# Импорт собсвтенных библиотек
import GenerModels.GigaChat as master
from GenerModels.API_T2I import *
from classes import *
from bot_commands.DnD_commands.create_character import *
import utils


symbols = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
sym = lambda: rdm.choice(symbols)
KEYS = os.environ.get("Api keys").split(";")

key = os.environ["BOT TOKEN"]
conversation_history = {}

bot = Bot(token=key, default = DefaultBotProperties(parse_mode = ParseMode.MARKDOWN))  # Мы инициализируем бота с ключом key, и устанавливаем некоторые свойства по умолчанию, здесь 
dsp = Dispatcher()

api = Text2ImageAPI('https://api-key.fusionbrain.ai/', KEYS[0], KEYS[1])
model_id = api.get_model()
user_id = ""
last_message = ""
rooms = {

}
RP_games = {
    "choiced": "",
    "D&D": {
        "Description": "Фэнтези, Подземелья и драконы, сказочные персонажи, приключения и бои.",
        "SystemDescription": "Ты - ведущий игры Dungeons & Dragons. Ты увлекательно и подробно рассказываешь истории, выбираешь необычные пути развития сюжета.",
        },
    "a": 1
}
history = []
users = {

}
fsm_states.append(users)
dsp.message.register(get_nickname, F.text, fsm_states[0])
dsp.message.register(get_class, F.text, fsm_states[1])
dsp.message.register(get_race, F.text, fsm_states[2])
# dsp.message.register(get_race, F.text, fsm_states[2], flags={"users": users})
@dsp.message(fil.Command(commands=['start', 's']))
async def bot_message(message):
    global user_id
    user_id = message.chat.id
    users[user_id] = {"characters": []}
    print(user_id)
    DnD = types.InlineKeyboardButton(text='🐲 Drag & Dung ⚔', callback_data='D&D')
    soon = types.InlineKeyboardButton(text="Скоро.", callback_data="soon")
     # Создаем объект инлайн-клавиатуры
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[DnD, soon]])
    print("\n", markup, "\n")
    await message.answer(
            text="Я бот для командных настольных игр. Но со мной они станут в разы интереснее!\nЧтобы ознакомиться с правилами введите `/help` или `/h`.\nЧтобы войти в меню игр введите `/menu`",
            reply_markup=markup
    )
#    bot.send_message(message.chat.id, "Я бот для командных настольных игр. Но со мной они станут в разы интереснее!\nЧтобы ознакомиться с правилами введите <code>/help</code> или <code>/h</code>.\nЧтобы войти в меню игр введите <code>/menu</code>", parse_mode='html', reply_markup=markup)

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'D&D' или "Скоро."
@dsp.callback_query(F.data.in_(['D&D', "Скоро."]))
async def processing_call(callback: types.CallbackQuery, state: FSMContext):
    print("Я тут, но другой босс!")
    if callback.data == "D&D":
        id = callback.message.chat.id
        print(state)
        await state.set_state(fsm_states[0])  # Наличие await Обязательно, без него программа пойдет дальше и произойдет ошибка
        await callback.message.answer("Как звать вас-то в игре?")
        print(callback.message.text)
         # await state.get_state()
         # await state.set_state()
         # await state.get_state()
        print(users)
        determine_DnD(users[id])
    elif callback.data == "soon":
        print("В разработке")
        await callback.answer()
def determine_DnD(user):
    global history
    history = [
                master.SystemMessage(
                    content=RP_games["D&D"]["SystemDescription"]
                )
            ]
    @dsp.message(fil.Command(commands=['menu', 'm']))
    async def join_to_menu(message: types.Message):
        print("УРАА")
        global user_id
        user_id = message.chat.id
        joiningRoom = types.InlineKeyboardButton(text='Присоединиться к комнате', callback_data='joinRoom')
        createRoom = types.InlineKeyboardButton(text="Создать свою комнату", callback_data="createRoom")
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[joiningRoom, createRoom]])
        await message.answer(  # В данном методе не нужно указывать ID, так как он работает следующим образом: метод .answer() 
                         # принимает параметр self (= message), а затем вызывает функцию SendMessage(self.chat.id), что = message.chat.id
            text="Вы зашли в меню. Вы можете <b>создать свою комнату</b> или <b>присоединиться к комнате.</b>", 
            reply_markup=markup
            )
        global last_message
        last_message = message

     # Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
     # с data 'D&D' или "Скоро."
    @dsp.callback_query(F.data.in_(['joinRoom', "createRoom"]))
    async def processing_callback(callback: types.CallbackQuery):
        print("я тут босс!")
        if callback.data == "joinRoom":
            callback.message.answer(
                text='Введите секретный ID для подключения (Добавив Code).\nНапример, Code: yyyyyyy'
                )
        elif callback.data == "createRoom":
            Id = eval(("sym()+ " * 9)[:-2])  # Это равнозначно вызову sym() 9 раз. В результате получаем строку 'sym()+ g...+ sym() +', поэтому берем всё, коме последнего знака ([:-2])
            await create_room(callback.message, Id)

    global processing_call
     # processing_call  # Удаляем первоначальную функцию "Обработка данных", чтобы избежать неполадок в будущем и чтобы в будущем она не вызывалась
    
    def join_to_room(user_id, Id):
        global rooms
        all_players = ", ".join(list(map(lambda x: str(x)[1:-1], [rooms[x]["players"] for x in rooms]))).split(", ")
        print(all_players)
        if str(user_id) not in all_players:
            user = [user for user in users if user == user_id][0]  # Здесь, нам необходим такой синтаксис по причине: приминить цикл for и if в одной строке можно 
                         # только заключив их в []. Они создадут список с юзерами.id == this_id, а такой элемент может быть всего один, значит, и элементов с списке 1
            rooms[Id]["players"].append(user)
        else:  # Иначе | =, если игрок состоит в команде
            if rooms[Id]["Status"] == True:  # Если игра началась, то 
                pass  # игнорируем, чтобы создать видимость, что функция больше не доступна
            else:  # иначе | если игра не началась
                bot.send_message(chat_id=user_id, text='Вы уже состоите в комнате.', parse_mode="html")
        print("Ты вошел в комнату!", Id)
    async def create_room(message: types.Message, Id: str):
        global rooms
        all_players = ", ".join(list(map(lambda x: str(x)[1:-1], [rooms[x]["players"] for x in rooms]))).split(", ")
        if str(message.chat.id) not in all_players:
            user = [user for user in users if user == message.chat.id][0]  # Здесь, нам необходим такой синтаксис по причине: приминить цикл for и if в одной строке можно 
                         # только заключив их в []. Они создадут список с юзерами.id == this_id, а такой элемент может быть всего один, значит, и элементов с списке 1
            await message.answer(
                text=f'Вот ваш ID для комнаты: `{Id}`'
                )
            rooms[Id] = {   
                            "players": [user],  # Список пользователей
                            "owner": user,  # Создатель комнаты
                            "Game": "D&D",  # Выбранная игра
                            "Status": False,  # Статус игры: началась - True, иначе - False
                            "Cur Step": "Next",  # Текущий шаг. Нужен "для баланса вселенной" и для того, чтобы игроки не совершали действия в неподходящие моменты.
                            "banned": []  # Список забаненных пользователей
                        }
            print("Ты создал комнату!", rooms)
            print(rooms)
        else:  # Иначе | =, если игрок состоит в команде
            if Id in rooms and rooms[Id]["Status"] == True:  # Если игра началась и id комнаты уже существует (->, не новый), то 
                pass  # игнорируем, чтобы создать видимость, что функция больше не доступна
            else:  # иначе | если игра не началась
                bot.send_message(chat_id=user_id, text='Вы уже состоите в комнате.', parse_mode="html")
    @dsp.message(fil.Command(commands=["game", "g"]))
    async def start_game(message: types.Message):
        for Id in rooms:
            if message.chat.id == rooms[Id]["owner"]:  # Проверяем, является ли владельцем комнаты человек, который написал эту команду
                if len(rooms[Id]["players"]) > 1:
                    rooms[Id]["Status"] = True
                    for user in rooms[Id]["players"]:
                         # Удаляем каждое сообщение
                        for m in history:
                            print(m)
                             # bot.delete_message(user, m.message_id)
                        await bot.send_message(user, text="Вы начали игру! Надеюсь, вы знакомы с правилами.")
                    break
                else:
                    await bot.send_message(message.chat.id, text="Вы не можете начать игру, так как вы один!")
                    break
    @dsp.message()
    async def general_chat(message: types.Message):
        user = [user for user in users if user == message.chat.id][0]
        if message.text.startswith("Code: "):
            print("Ура! Победа")
            join_to_room(user_id=user, Id=message.text[6:])
        from_bot = ""
        for room in rooms:
            room = rooms[room]
            if user in room["players"]:  # Если игрок в этой комнате
                if room["Status"] == True:  # и если игра началась, 
                                             # то можно проверять команды ниже
                    if message.text.startswith("Result: ") and user == room["owner"] and room["Cur Step"] == "Result":
                        pass
                         # history.append(master.HumanMessage(content=message.text[8:]))
                        room["Cur Step"] = "Next"
                    elif message.text.startswith("Next: ") \
                                    and user == room["owner"] \
                                    and room["Cur Step"] == "Next":
                        history.append(master.HumanMessage("Что мы будем делать дальше и куда идти? Расскажи подробно и увлекающее. Придумай интересный квест."))
                        from_bot = history[-1].content
                        room["Cur Step"] = "Result"
                for player in room["players"]:
                    if player != message.chat.id:  # Так как Player - это объект класса Player..., у него есть свойство id, по которому мы проверяем пользователя
                        message_in_game = f'''<i>{users[user[0]].nickname}</i> - {users[user[0]].ClassHero[1]}-{users[user[0]].raceHero[1]}
                                            {message.text}'''
                        await bot.send_message(chat_id=player, text=message_in_game)
                    if from_bot:
                        await bot.send_message(chat_id=player, text=from_bot)
                    print(message.message_id)
                
                history.append(message)
                print(history)
        # if message.text:
        #     user_id = message.from_user.id
        #     user_input = message.text
        #     if user_id not in conversation_history:
        #         conversation_history[user_id] = []

        #     conversation_history[user_id].append({"role": "user", "content": user_input})

        #     chat_history = conversation_history[user_id]
        #     print(chat_history)
        #     try:
        #         response = asyncio.run(g4f.ChatCompletion.create_async(
        #             model=g4f.models.default,
        #             messages=chat_history,
        #             provider=g4f.Provider.GeekGpt,
        #         ))
        #         chat_gpt_response = response
        #     except Exception as e:
        #         print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        #         chat_gpt_response = "Извините, произошла ошибка."
        #     await bot.send_message(message.chat.id, chat_gpt_response)
            # print(message.text)
            # prompt = message.text
            # uuid = api.generate(prompt, model_id)
            # images = api.check_generation(uuid)
            # # Здесь image_base64 - это строка с данными изображения в формате base64
            # image_base64 = images[0] # Вставьте вашу строку base64 сюда
            # # Декодируем строку base64 в бинарные данные
            # image_data = base64.b64decode(image_base64)
            # with open("info.txt", "w+") as file:
            #     file.write(f"{image_base64} in this {images[len(images)-1]}\n")
            # # Открываем файл для записи бинарных данных изображения
            # with open("image.jpg", "wb") as file:
            #     file.write(image_data)
            #     print("AAA")
            # img = open("image.jpg", 'rb')
            # bot.send_photo(message.chat.id, img)
            # print(img)
		
print("All working")
dsp.run_polling(bot)
