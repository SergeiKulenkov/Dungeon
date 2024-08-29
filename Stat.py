import Config
import pygame
from Game import SCREEN

class Stat:
    def __init__(self, name, value, colour):
        self.value = value
        self.name = name
        self.colour = colour

        STAT_FONT = pygame.font.SysFont(Config.FONT, Config.STAT_TEXT_SIZE)
        self.nameText = STAT_FONT.render(self.name, 1, self.colour)
        self.valueText = STAT_FONT.render(str(self.value), 1, self.colour)

    def drawName(self, positionX, positionY):
        SCREEN.blit(self.nameText, (positionX, positionY))

    def drawValue(self, positionX, positionY):
        SCREEN.blit(self.valueText, (positionX, positionY))

    def getNameWidth(self):
        return self.nameText.get_width()

    def getValueWidth(self):
        return self.valueText.get_width()
