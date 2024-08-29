from enum import Enum
from Stat import Stat

class EnemyType:
    SKELETON = 1
    GOBLIN = 2
    ORC = 3
    SPIDER = 4

class Enemy:
    def __init__(self, type):
        self.type = type
        self.stats = []

        match type:
            case EnemyType.SKELETON:
                for name, value in Config.SKELETON_STATS.items():
                    self.stats.append(Stat(name, value, Config.STATS_COLOURS[name]))

    # draw image and stats