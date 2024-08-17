class Player:
    def __init__(self, id, game) -> None:
        self.choiced_game = game
        self.id = id
class DnDPlayer(Player):
    class Class:
        '''Супер-класс для всех подклассов персонажей. Инициализирует общие свойства:
        \n\t Броня, сила, ловкость, телосложение, интеллект, мудрость, харизма.'''
        def __init__(self, damage,
                        armor: dict[str, int],
                        strenght: int,
                        dexterity: int,
                        physique: int,
                        intelligence: int,
                        wisdom: int,
                        charisma: int):
            self.damage = 1
            self.cls_armor = armor
            self.level = 1
            self.power = strenght
            self.dexterity = dexterity
            self.physique = physique
            self.intelligence = intelligence
            self.wisdom = wisdom
            self.charisma = charisma
    class Warrior(Class):
        def __init__(self):
            super().__init__(1, 0, 8, 8, 8, 8, 8, 8)   
        def second_wind(self):
            '''Если вы в свой ход совершаете действие Атака, вы можете совершить две атаки вместо одной.
                \nКоличество атак увеличивается до трёх на 11-м уровне этого класса, и до четырёх на 20-м уровне.'''
            if self.level >= 5:
                pass

    class Barbarian(Class):
        def __init__(self):
            super().__init__()
        def protection_without_armor(self):
            '''Если вы не носите доспехов, ваш Класс Доспеха равен 10 + модификатор Ловкости + модификатор Телосложения. 
            Вы можете использовать щит, не теряя этого преимущества.'''
            if self.level >= 1:
                if len(self.armor) == 0:
                    self.cls_armor = 10 + (self.dexterity - 6) + (self.physique - 6)
    class Ranger(Class):
        def __init__(self):
            super().__init__()
    class Sorcerer(Class):
        def __init__(self):
            super().__init__()
    class Cleric(Class):
        def __init__(self):
            super().__init__()
    class Bard(Class):
        def __init__(self):
            super().__init__()
    class Monk(Class):
        def __init__(self):
            super().__init__()
    class Paladin(Class):
        def __init__(self):
            super().__init__()
    class Artificer(Class):
        def __init__(self):
            super().__init__()
    class Wizard(Class):
        def __init__(self):
            super().__init__()
    class Druid(Class):
        def __init__(self):
            super().__init__()
    class Rogue(Class):
        def __init__(self):
            super().__init__()
    class Warlock(Class):
        def __init__(self):
            super().__init__()
    
    
    def __init__(self,
                 id: int, 
                 game: str, 
                 nickname: any, 
                 type="Warrior", 
                 race="Human"):
        '''Инициализирует экземпляр класса "Игрок D&D".
            \n\tСвойство game всегда равно D&D.
            \n\tСвойство nickname равно введенному нику.
            \n\tОстальные свойства не обязательны, по умолчанию это "Воин-Человек"'''
        Player.__init__(self, id=id, game=game)
        self.nickname = nickname
        self.ClassHero = (
            eval(f"self.{type}()"),
            type)
        print(self.ClassHero)
        self.raceHero = (
            race,
            race)
        print(self.raceHero)
    def roll_dice(self, sides: int | None = 6):
        pass
    def attack(self, enemy, damage):
        number = self.roll_dice(20)
        if number == 1:
            return f"Ваше число {number}. Вы промахнулись и не нанесли урон!"
        elif number == 20:

            return f"Ваше число {number}. Вы нанесли критический удар!"