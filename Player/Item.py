from enum import Enum
import pygame
import os.path
import random

from Game.Config import GeneralConfig
from Game.Config import ItemsConfig
from Game.Game import SCREEN
from Game.Game import DOOR_POSITION_X
from Game.Game import DOOR_POSITION_Y

class ItemType(Enum):
    BOW = 0
    BOMB = 1
    AXE = 2
    MAGIC_SCROLL = 3
    TREASURE = 4

class Item:
    BOW_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, ItemsConfig.BOW_IMAGE))
    BOMB_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, ItemsConfig.BOMB_IMAGE))
    AXE_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, ItemsConfig.AXE_IMAGE))
    SCROLL_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, ItemsConfig.SCROLL_IMAGE))
    TREASURE_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, ItemsConfig.TREASURE_IMAGE))

    def __init__(self, isArtifact: bool):
        self._type = ItemType.BOW
        self._image: pygame.Surface = None
        self._power = 0

        if not isArtifact:
            self._type = ItemType(random.randint(ItemType.BOW.value, ItemType.AXE.value))
        else:
            self._type = ItemType(random.randint(ItemType.MAGIC_SCROLL.value, ItemType.TREASURE.value))

        match self._type:
            case ItemType.BOW:
                self._power = ItemsConfig.BOW_POWER
                self._image = pygame.transform.scale(Item.BOW_IMAGE, (ItemsConfig.ITEM_WIDTH, ItemsConfig.ITEM_HEIGHT))
            case ItemType.BOMB:
                self._power = ItemsConfig.BOMB_POWER
                self._image = pygame.transform.scale(Item.BOMB_IMAGE, (ItemsConfig.ITEM_WIDTH, ItemsConfig.ITEM_HEIGHT))
            case ItemType.AXE:
                self._power = ItemsConfig.AXE_POWER
                self._image = pygame.transform.scale(Item.AXE_IMAGE, (ItemsConfig.ITEM_WIDTH, ItemsConfig.ITEM_HEIGHT))
            case ItemType.MAGIC_SCROLL:
                self._power = ItemsConfig.MAGIC_SCROLL_POWER
                self._image = pygame.transform.scale(Item.SCROLL_IMAGE, (ItemsConfig.ITEM_WIDTH, ItemsConfig.ITEM_HEIGHT))
            case ItemType.TREASURE:
                self._image = pygame.transform.scale(Item.TREASURE_IMAGE, (ItemsConfig.ITEM_WIDTH, ItemsConfig.ITEM_HEIGHT))

        self._isSingleUse = (self._type is ItemType.BOW or self._type is ItemType.BOMB or self._type is ItemType.MAGIC_SCROLL)
        self._position = pygame.math.Vector2(DOOR_POSITION_X + GeneralConfig.DOOR_WIDTH / 2 - ItemsConfig.ITEM_WIDTH / 2,
                                             DOOR_POSITION_Y + GeneralConfig.DOOR_HEIGHT / 2 - ItemsConfig.ITEM_HEIGHT / 2)

    @property
    def isSingleUse(self):
        return self._isSingleUse

    @property
    def type(self):
        return self._type

    @property
    def power(self):
        return self._power

    def changePosition(self, newPosition: pygame.math.Vector2):
        self._position = pygame.math.Vector2(newPosition)

    def changeScaleForInventory(self):
        if self._image is not None:
            self._image = pygame.transform.scale(self._image, (ItemsConfig.ITEM_WIDTH_INVENTORY, ItemsConfig.ITEM_HEIGHT_INVENTORY))

    def draw(self):
        if self._image is not None:
            SCREEN.blit(self._image, self._position)