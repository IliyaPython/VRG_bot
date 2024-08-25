CLASSES = {
    "Warrior": ["warrior", "воин", "base", "база"],
    "Barbarian": ["barbarian", "варвар"],
    "Ranger": ["ranger", ""],
    "Sorcerer": ["sorcerer"],
    "Cleric": ["cleric"],
    "Bard": ["bard", "бард"],
    "Monk": ["monk", "монах"],
    "Paladin": ["paladin"],
    "Artificer": ["artificer", "инженер"],
    "Wizard": [
        "wizard",
    ],
    "Druid": ["druid"],
    "Rogue": ["rogue"],
    "Warlock": ["warlock"],
}


class Class:
    """Супер-класс для всех подклассов персонажей. Инициализирует общие свойства:
    \n\t Броня, сила, ловкость, телосложение, интеллект, мудрость, харизма."""

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


class Warrior(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)

    def second_wind(self):
        """Если вы в свой ход совершаете действие Атака, вы можете совершить две атаки вместо одной.
        \nКоличество атак увеличивается до трёх на 11-м уровне этого класса, и до четырёх на 20-м уровне.
        """
        if self.level >= 5:
            pass


class Barbarian(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)

    def protection_without_armor(self):
        """Если вы не носите доспехов, ваш Класс Доспеха равен 10 + модификатор Ловкости + модификатор Телосложения.
        Вы можете использовать щит, не теряя этого преимущества."""
        if self.level >= 1:
            if len(self.armor) == 0:
                self.cls_armor = 10 + (self.dexterity - 6) + (self.physique - 6)


class Ranger(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Sorcerer(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Cleric(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Bard(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Monk(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Paladin(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Artificer(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Wizard(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Druid(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Rogue(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)


class Warlock(Class):
    def __init__(self):
        super().__init__(1, 0, 8, 8, 8, 8, 8, 8)
