from enum import Enum
from Character import Character
# from Game import SCREEN

class CharacterType(Enum):
    DEFAULT = 1

class Player:
    def __init__(self, type):
        self.score = 0
        match type:
            case CharacterType.DEFAULT:
                self.character = Character()
            case _:
                self.character = Character()

    def draw(self):
        self.character.drawStats()