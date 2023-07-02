from enum import Enum


class Colors(Enum):
    WHITE = 1
    BLACK = 2
    RED = 3
    BLUE = 4
    GREEN = 5
    YELLOW = 6
    ORANGE = 7
    PURPLE = 8
    BROWN = 9
    GRAY = 10
    NAVY = 11
    TEAL = 12
    LIGHT_BLUE = 13
    GOLD = 14

    def __repr__(self):
        return self.name.lower()

    def __str__(self):
        return self.name.lower()
