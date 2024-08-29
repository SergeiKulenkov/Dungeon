from enum import Enum
import Config
import pygame
import os.path
from Game import SCREEN
from Game import DOOR_POSITION_X
from Game import DOOR_POSITION_Y

BOW_IMAGE = pygame.image.load(os.path.join(Config.IMAGES_PATH, Config.BOW_IMAGE))
BOW = pygame.transform.scale(BOW_IMAGE, (Config.ITEM_WIDTH, Config.ITEM_HEIGHT))

class ItemType(Enum):
    BOW = 1
    BOMB = 2
    AXE = 3

class Item:
    def __init__(self):
        self.type = 1

    def draw(self):
        # add calculation for position via item width
        SCREEN.blit(BOW, (DOOR_POSITION_X, DOOR_POSITION_Y))