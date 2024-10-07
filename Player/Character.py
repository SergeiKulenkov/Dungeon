import pygame

from Game.Config import CharacterConfig
from Game.Config import StatsConfig
from Game.Game import BORDER_STATS
from Player.Item import Item
from Player.Item import ItemType
from Player.Stat import Stat

class Character:
    def __init__(self):
        self._stats: list[Stat] = []
        self._statPosition = pygame.math.Vector2(StatsConfig.STATS_OFFSET_FROM_BORDER_X,
                                            BORDER_STATS.y + StatsConfig.STATS_OFFSET_FROM_BORDER_Y)

        for name, value in CharacterConfig.BASE_STATS.items():
            self._stats.append(Stat(name, value, self._statPosition))
            self._statPosition.x = self._stats[-1].getEndPosition() + StatsConfig.STATS_GAP

        self._item: Item = None

    @property
    def itemType(self) -> ItemType:
        return self._item.type

    @property
    def damage(self) -> int:
        damage = 0
        for stat in self._stats:
            if stat.getName() is StatsConfig.DAMAGE_STAT_NAME:
                damage = stat.getValue()
                break

        return damage

    @property
    def itemPower(self) -> int:
        return self._item.power

    @property
    def luck(self) -> int:
        luck = 0
        for stat in self._stats:
            if stat.getName() is StatsConfig.LUCK_STAT_NAME:
                luck = stat.getValue()
                break

        return luck

    def changeHealth(self, hp: int) -> bool:
        isChanged = False
        for stat in self._stats:
            if stat.getName() is StatsConfig.HEALTH_STAT_NAME:
                if hp > 0:
                    hpDifference = CharacterConfig.BASE_STATS[StatsConfig.HEALTH_STAT_NAME] - stat.getValue()
                    if hpDifference > 0:
                        stat.changeValue(min(hpDifference, hp))
                        isChanged = True
                else:
                    stat.changeValue(hp)
                    isChanged = True
                break

        return isChanged

    def changeDamage(self, damage: int):
        for stat in self._stats:
            if stat.getName() is StatsConfig.DAMAGE_STAT_NAME:
                stat.changeValue(damage)
                break

    def isAlive(self) -> bool:
        isAlive = True
        for stat in self._stats:
            if stat.getName() is StatsConfig.HEALTH_STAT_NAME:
                isAlive = stat.getValue() > 0
                break

        return isAlive

    def changeItem(self, item: Item):
        self._item = item
        self._item.changePosition(pygame.math.Vector2(self._statPosition.x + CharacterConfig.ITEM_OFFSET_FROM_STATS_X,
                                                    BORDER_STATS.y + StatsConfig.STATS_OFFSET_FROM_BORDER_Y))
        self._item.changeScaleForInventory()

    def removeItem(self):
        self._item = None

    def drawStats(self):
        for stat in self._stats:
            stat.draw()

    def drawItem(self):
        if self._item is not None:
            self._item.draw()