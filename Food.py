import pygame
import os.path
import random

from Config import GeneralConfig
from Config import FoodConfig
from Game import SCREEN
from Game import DOOR_POSITION_X
from Game import DOOR_POSITION_Y

class Food:
    FOOD_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, FoodConfig.FOOD_IMAGE))

    def __init__(self):
        self._image: pygame.Surface = pygame.transform.scale(Food.FOOD_IMAGE, (FoodConfig.FOOD_WIDTH, FoodConfig.FOOD_HEIGHT))
        self._position = pygame.math.Vector2(DOOR_POSITION_X + GeneralConfig.DOOR_WIDTH / 2 - FoodConfig.FOOD_WIDTH / 2,
                                             DOOR_POSITION_Y + GeneralConfig.DOOR_HEIGHT / 2 - FoodConfig.FOOD_HEIGHT / 2)

    def getHP(self) -> int:
        return random.randint(FoodConfig.MIN_HP, FoodConfig.MAX_HP)

    def draw(self):
        SCREEN.blit(self._image, (self._position.x, self._position.y))