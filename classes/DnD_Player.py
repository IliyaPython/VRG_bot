from .DND_Staff.ClassResource import *
from .DND_Staff.RaceResource import *

class DnDPlayer:
    """Класс D&D Player, инициализирует игрока игры D&D.
        Требует параметры ID, nickname."""
    def __init__(self, 
                ID: int,
                nickname: str,
                gClass: str = "Warrior",
                race: str = "Human"):
        self.ID = ID
        self.nickname = nickname
        self.HeroClass = (
            eval(f"{gClass}()"),
            gClass
        )
        self.race = (
            eval(f"{race}()"),
            race
        )
    def roll_dice(self, sides: int | None = 6):
        pass
    def attack(self, enemy, damage):
        number = self.roll_dice(20)
        if number == 1:
            return f"Ваше число {number}. Вы промахнулись и не нанесли урон!"
        elif number == 20:

            return f"Ваше число {number}. Вы нанесли критический удар!"