import uuid

from classes.DND_Staff import dyces
from classes import Room
from .DND_Staff.ClassResource import *
from .DND_Staff.RaceResource import *


class DnDCharacter:
    """Класс D&D Player, инициализирует игрока игры D&D.

    :param ID: a
    :param nickname: a
    :param str gClass:
    :param str race:
    :param uuid:
    """

    def __init__(
        self,
        ID: int,
        nickname: str,
        gClass: str = "Warrior",
        race: str = "Human",
        uid: uuid.UUID = "New"
    ):
        self.ID = ID
        self.nickname = nickname
        self.HeroClass = (eval(f"{gClass}()"), gClass)
        self.race = (eval(f"{race}()"), race)
        self.room: Room = None
        # ИД персонажа равно указанному в uuid
        self.uuid = uid
        # Однако, только если персонаж новый, то создаём ему новый ИД
        if uid is "New":
            # Преобразовываем в строку новый ИД, чтобы была возможность сериализации ИД
            self.uuid = str(uuid.uuid1())

        # Создаём словарь с данными о данных объекта, который будем сохранять в Json, а затем воссоздавать персонажа по этому словарю
        self.__metadata__ = {
            "ID": ID,
            "nickname": nickname,
            "gClass": gClass,
            "race": race,
            "uuid": self.uuid
        }

    def attack(self, enemy, damage):
        number, photo = dyces.Dyce().dice20()
        if number == 1:
            return f"Ваше число {number}. Вы промахнулись и не нанесли урон!"
        elif number == 20:

            return f"Ваше число {number}. Вы нанесли критический удар!"
