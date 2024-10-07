import pygame
from Config import GeneralConfig
from Config import StatsConfig
from Game import SCREEN

class Stat:
    def __init__(self, name: str, value: int, position: pygame.math.Vector2):
        self._name = name
        self._value = value
        self._colour = StatsConfig.STATS_COLOURS[name]

        self._font = pygame.font.SysFont(GeneralConfig.FONT, StatsConfig.STAT_TEXT_SIZE)
        self._nameText = self._font.render(self._name, 1, self._colour)
        self._valueText = self._font.render(str(self._value), 1, self._colour)

        self._namePosition = pygame.math.Vector2(position)
        self._valuePosition = pygame.math.Vector2(position)
        self._valuePosition.x += self._nameText.get_width() + StatsConfig.STAT_VALUE_OFFSET

    def getEndPosition(self):
        return self._valuePosition.x + self._valueText.get_width()

    def getName(self) -> str:
        return self._name

    def getValue(self) -> int:
        return self._value

    def changeValue(self, change):
        self._value += change
        self._valueText = self._font.render(str(self._value), 1, self._colour)

    def draw(self):
        SCREEN.blit(self._nameText, (self._namePosition.x, self._namePosition.y))
        SCREEN.blit(self._valueText, (self._valuePosition.x, self._valuePosition.y))
