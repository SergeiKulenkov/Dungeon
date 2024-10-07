import pygame
import os.path

from Enemy.EnemyManager import EnemyType
from Player.Stat import Stat
from Game.Config import GeneralConfig
from Game.Config import StatsConfig
from Game.Config import EnemyConfig
from Game.Game import SCREEN
from Game.Game import DOOR_POSITION_X
from Game.Game import DOOR_POSITION_Y

class Enemy:
    SKELETON_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, EnemyConfig.SKELETON_IMAGE))
    GOBLIN_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, EnemyConfig.GOBLIN_IMAGE))
    ORC_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, EnemyConfig.ORC_IMAGE))
    SPIDER_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, EnemyConfig.SPIDER_IMAGE))

    def __init__(self, type):
        self._type: EnemyType = type
        self._stats: list(Stat) = []
        self._image: pygame.Surface = None
        self._position = pygame.math.Vector2(DOOR_POSITION_X + GeneralConfig.DOOR_WIDTH / 2 - EnemyConfig.ENEMY_WIDTH / 2,
                                             DOOR_POSITION_Y + GeneralConfig.DOOR_HEIGHT - EnemyConfig.ENEMY_HEIGHT)
        self._statPosition = pygame.math.Vector2(DOOR_POSITION_X + GeneralConfig.DOOR_WIDTH / 4 - StatsConfig.STATS_GAP,
                                                 DOOR_POSITION_Y - StatsConfig.STATS_OFFSET_FROM_BORDER_Y)

        match type:
            case EnemyType.SKELETON:
                self._image = pygame.transform.scale(Enemy.SKELETON_IMAGE, (EnemyConfig.ENEMY_WIDTH, EnemyConfig.ENEMY_HEIGHT))
                self._initializeStats(EnemyConfig.SKELETON_STATS)
            case EnemyType.GOBLIN:
                self._image = pygame.transform.scale(Enemy.GOBLIN_IMAGE, (EnemyConfig.ENEMY_WIDTH, EnemyConfig.ENEMY_HEIGHT))
                self._initializeStats(EnemyConfig.GOBLIN_STATS)
            case EnemyType.ORC:
                self._image = pygame.transform.scale(Enemy.ORC_IMAGE, (EnemyConfig.ENEMY_WIDTH, EnemyConfig.ENEMY_HEIGHT))
                self._initializeStats(EnemyConfig.ORC_STATS)
            case EnemyType.SPIDER:
                self._image = pygame.transform.scale(Enemy.SPIDER_IMAGE, (EnemyConfig.ENEMY_WIDTH, EnemyConfig.ENEMY_HEIGHT))
                self._initializeStats(EnemyConfig.SPIDER_STATS)

    @property
    def type(self) -> EnemyType:
        return self._type

    @property
    def damage(self) -> int:
        damage = 0
        for stat in self._stats:
            if stat.getName() is StatsConfig.DAMAGE_STAT_NAME:
                damage = stat.getValue()
                break

        return damage

    def _initializeStats(self, stats: dict[str, int]):
        for name, value in stats.items():
            self._stats.append(Stat(name, value, self._statPosition))
            self._statPosition.x = self._stats[-1].getEndPosition() + StatsConfig.STATS_GAP

    def isAlive(self) -> bool:
        isAlive = True
        for stat in self._stats:
            if stat.getName() is StatsConfig.HEALTH_STAT_NAME:
                isAlive = stat.getValue() > 0
                break

        return isAlive

    def takeDamage(self, damage: int):
        for stat in self._stats:
            if stat.getName() is StatsConfig.HEALTH_STAT_NAME:
                stat.changeValue(-damage)

    def draw(self):
        for stat in self._stats:
            stat.draw()

        if self._image is not None:
            SCREEN.blit(self._image, (self._position.x, self._position.y))