import Config
import pygame
# from Game import SCREEN
from Game import BORDER_STATS
from Item import Item
from Artifact import Artifact
from Stat import Stat

class Character:
    def __init__(self):
        self.stats = []
        for name, value in Config.BASE_STATS.items():
            self.stats.append(Stat(name, value, Config.STATS_COLOURS[name]))

        self.item = None
        self.artifact = None

    def drawStats(self):
        positionX = Config.STATS_OFFSET_FROM_BORDER_X
        positionY = BORDER_STATS.y + Config.STATS_OFFSET_FROM_BORDER_Y

        for stat in self.stats:
            stat.drawName(positionX, positionY)
            positionX += stat.getNameWidth() + Config.STAT_VALUE_OFFSET
            stat.drawValue(positionX, positionY)
            positionX += stat.getValueWidth() + Config.STATS_GAP