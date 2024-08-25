class Player:
    def __init__(self, id, game) -> None:
        self.choiced_game = game
        self.id = id


class DnDPlayer(Player):
    class Class:
        """Супер-класс для всех подклассов персонажей. Инициализирует общие свойства:
        \n\t Броня, сила, ловкость, телосложение, интеллект, мудрость, харизма.
        """

        def __init__(
            self,
            damage,
            armor: dict[str, int],
            strenght: int,
            dexterity: int,
            physique: int,
            intelligence: int,
            wisdom: int,
            charisma: int,
        ):
            self.damage = 1
            self.cls_armor = armor
            self.level = 1
            self.power = strenght
            self.dexterity = dexterity
            self.physique = physique
            self.intelligence = intelligence
            self.wisdom = wisdom
            self.charisma = charisma

    def __init__(
        self, id: int, game: str, nickname: any, type="Warrior", race="Human"
    ):
        """Инициализирует экземпляр класса "Игрок D&D".
        \n\tСвойство game всегда равно D&D.
        \n\tСвойство nickname равно введенному нику.
        \n\tОстальные свойства не обязательны, по умолчанию это "Воин-Человек"
        """
        Player.__init__(self, id=id, game=game)
        self.nickname = nickname
        self.ClassHero = (eval(f"self.{type}()"), type)
        print(self.ClassHero)
        self.raceHero = (race, race)
        print(self.raceHero)

    def roll_dice(self, sides: int | None = 6):
        pass

    def attack(self, enemy, damage):
        number = self.roll_dice(20)
        if number == 1:
            return f"Ваше число {number}. Вы промахнулись и не нанесли урон!"
        elif number == 20:

            return f"Ваше число {number}. Вы нанесли критический удар!"
