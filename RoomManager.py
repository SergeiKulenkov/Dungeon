from enum import Enum
import pygame
import random
import Config
from Game import SCREEN
from Item import Item
from ActionLogManager import ActionLogManager
from EnemyManager import EnemyManager

class RoomType(Enum):
    COMBAT = 1
    TREASURE = 2
    ITEM = 3

class RoomManager:
    def __init__(self):
        self.roomIndex = 0
        self.currentRoomType = RoomType.ITEM
        # remove from class variables
        self.actionLogManager = ActionLogManager()
        self.enemyManager = EnemyManager()

    # event
    def generateRoom(self):
        self.currentRoomType = random.randint(1, 3)
        # event
        self.actionLogManager.onRoomEntered()

    def drawRoom(self):
        self.actionLogManager.drawLogs()

        match self.currentRoomType:
            case RoomType.COMBAT:
                self.enemyManager.spawnEnemy()
            case RoomType.TREASURE:
                item = Item()
                item.draw()
            case RoomType.ITEM:
                item = Item()
                item.draw()
