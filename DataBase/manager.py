import json
from typing import Union

async def read_database(database: str) -> dict[str, dict]:
    # TODO: Рассмотреть способ сделать так, чтобы ключив возвращаемом словаре db были цифрами, а не стркоами.
    #*  это сильно облегчит взаимодействие между кодом и базой.
    with open(f"DataBase/{database}.json", "r") as database:
        db = json.load(database)
        print(db)
    return db


async def init_object(data: dict[str, any],
                      working_class: any) -> any:
    """Инициализирует / воссоздаёт объект класса {working_class} по\n
        сохранённым данным из {data}.
        
    :params dict[str, any] data: Словарь с данными в стиле {"свойство": значение}
    :params any working_class: Класс, через который будет создаваться нужный объект
    :return temp (any): Объект класса (хоть и отличается сам объект, все данные идентичны)
        """
    temp = working_class(**data)
    return temp


async def add_user(ID: str):
     if ID:

        with open("DataBase/users.json", "r") as database:
            users = json.load(database)

            if ID not in users.keys():
                users[ID] = {
                    "Characters": list(),
                    "Current Character": None
                }

        with open("database/users.json", "w") as database:
            json.dump(users, database, indent=4)


async def get_characters_by_ID(ID: int,
                               returnNames: bool = False) -> list[any]:
    """
    На вход получает ID пользователя. Открывает базу данных и ищет совпадения по ID.\n
    Далее возвращает список персонажей из базы - database[user_id]["characters"]

    :param int ID: принимает только ID пользователя (message.chat.id)
    :param bool returnNames: Необязательно. Если равно True, то возвращает кортеж (ID, nickname)
    :return list[uuid]: возвращает список со всеми ID персонажей пользователя."
    """

    if ID:
        ID = str(ID) #* В json доступны только строковые ключи
        
        with open("database/users.json", "r") as database:
            users = json.load(database)
            print(users)
            print(ID)
            if (
                ID in users.keys()
            ):  # Проверяем, есть ли ID в ключах словаря. Ключами словаря являются ID пользователей. Фактически, проверка есть ли пользователь
                print("ID EXISTS")
                if returnNames:
                    temp = list(map(
                        # Получаем self и nickname персонажа в новый список (x - слоаврь с данными о char (char.__metadata__))
                        lambda x: (x.get("uuid"), x.get("nickname")),
                        users[ID]["Characters"]
                        )
                    )
                    return temp
                temp = list(map(
                    lambda x: x.get("uuid"), # Возвращает uuid персонажа
                    users[ID]["Characters"]
                ))
                print("TEMP TEST ---", temp)
                return temp


async def get_character_by_UID(user_id: int,
                               UID: str) -> dict[str, any]:
    """Получаёт ИД текущего пользователя и УН. ИД для персонажа.
        # Логика:
            1. Читает базу данных и ищет в ней список всех персонажей юзера
            2. Проходит по всему списку персонажей, и если найдено совпадение, возвращает словарь с данными о персонаже
            3. Иначе, возникает ошибка `Exception: Персонаж не найден. UID не найдено в списке персонажей пользователя`
        # Returns: dict[str, any]
    """
    users = await read_database("users")
    user_id = str(user_id) #* В json доступны только строковые ключи
    #! Первая версия
    characters = users[user_id]["Characters"]

    for char in characters:
        if char.get("uuid") == UID:
            return char
    
    # Если персонаж найден, то программа завершится ещё в 93 строчке. Следовательно, если продолжит работу, значит не найден
    raise Exception(f"Персонаж не найден. UID не найдено в списке персонажей пользователя {user_id}")
    #! Вторая версия
    # characters = await get_characters_by_ID(user_id)
    
    # try:
    #     index = characters.index(UID) # Поиск UID в списке всех UID для персонажей
    # except ValueError:
    #     raise Exception(f"Персонаж не найден. UID не найдено в списке персонажей пользователя {user_id}")
    
    # char = users[user_id]["Characters"][index]
    # return char


async def replace_data_user(ID: int,
                            key: Union[str, int, tuple, bool],
                            new_value: any,
                            subkey: Union[str, int, tuple, bool] = None):
    """
    На вход получает ключ, который надо заменить на новое значение.\n
    Если нужен доп. ключ, укажите в subkey.

    :param int ID: принимает только объект ID пользователя
    :param key: принимает ключ, который будет заменён.
    :param new_value: новое значение
    :param Optional subkey: доп. ключ для словаря | списка в database[user_id][key]
    :return Character: возвращает список со всеми персонажами пользователя, персонажы являются объектами {game}Character"
    """

    if ID:
        ID = str(ID) #* В json доступны только строковые ключи

        with open("database/users.json", "r") as database:
            users = json.load(database)
            print(users)
            try:
                if not (subkey == None):
                    print("NOO")
                    users[ID][key][subkey] = new_value
                else:
                    print("YEES")
                    users[ID][key] = new_value
            except:
                print("Some error ocurred in func \"replace_data_user\"")
        
        with open("database/users.json", "w") as database:
            json.dump(users, database) # Перезаписываем новую базу данных, которую мы обновили выше