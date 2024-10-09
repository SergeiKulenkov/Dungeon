from enum import Enum
import pygame
import random
import copy
from Game.Config import RoomConfig

class RoomEvents:
    roomGeneratedEventType = pygame.event.custom_type()
    foodEatenEventType = pygame.event.custom_type()
    itemTakenEventType = pygame.event.custom_type()

class RoomType(Enum):
    COMBAT = 0
    FOOD = 1
    ITEM = 2

from Game.Game import subscribeToEvent
from Game.Game import GameEvents
from Player.Food import Food
from Player.Item import Item
from Button.ButtonManager import ButtonEvents
from Button.ButtonManager import ButtonType

class RoomManager:
    def __init__(self):
        self._currentRoomType: RoomType = None
        self._roomEvent: Food | Item = None
        self._itemsInRow = 0
        self._foodInRow = 0

        self._roomGeneratedEvent = pygame.event.Event(RoomEvents.roomGeneratedEventType, { RoomConfig.ROOM_TYPE_VALUE : None })
        self._foodEatenEvent = pygame.event.Event(RoomEvents.foodEatenEventType, { RoomConfig.FOOD_HP_VALUE : 0 })
        self._itemTakenEvent = pygame.event.Event(RoomEvents.itemTakenEventType, { RoomConfig.ITEM_VALUE : None })

        subscribeToEvent(GameEvents.gameStartedEventType, self._onGameStarted)
        subscribeToEvent(GameEvents.roomEnteredEventType, self._generateRoom)
        subscribeToEvent(ButtonEvents.buttonPressedEventType, self._handleButtonPress)

    def reset(self):
        self._itemsInRow = 0
        self._foodInRow = 0

    def _onGameStarted(self):
        self._generateRoom()

    def _generateRoom(self):
        randomProbability = random.random()
        for name, probability in RoomConfig.ROOMS_CONTENTS_PROBABILITIES.items():
            randomProbability -= probability
            if randomProbability <= 0:
                self._currentRoomType = RoomType.__getitem__(name)
                break

        if self._itemsInRow >= RoomConfig.MAX_ITEMS_IN_ROW:
            self._currentRoomType = RoomType.COMBAT
            self._itemsInRow = 0
        if self._foodInRow >= RoomConfig.MAX_FOOD_IN_ROW:
            self._currentRoomType = RoomType.COMBAT
            self._foodInRow = 0

        match self._currentRoomType:
            case RoomType.FOOD:
                self._foodInRow += 1
                self._roomEvent = Food()
            case RoomType.ITEM:
                self._itemsInRow += 1
                chance = random.random()
                if RoomConfig.ARTIFACT_PROBABILITY >= chance:
                    self._roomEvent = Item(True)
                else:
                    self._roomEvent = Item(False)
            case _:
                self._roomEvent = None

        self._roomGeneratedEvent.dict[RoomConfig.ROOM_TYPE_VALUE] = self._currentRoomType
        pygame.event.post(self._roomGeneratedEvent)

    def _handleButtonPress(self, buttonType: ButtonType):
        match buttonType:
            case ButtonType.EAT:
                if isinstance(self._roomEvent, Food):
                    self._foodEatenEvent.dict[RoomConfig.FOOD_HP_VALUE] = self._roomEvent.getHP()
                    pygame.event.post(self._foodEatenEvent)
            case ButtonType.TAKE_ITEM:
                if isinstance(self._roomEvent, Item):
                    self._itemTakenEvent.dict[RoomConfig.ITEM_VALUE] = copy.copy(self._roomEvent)
                    pygame.event.post(self._itemTakenEvent)

    def drawRoom(self):
        match self._currentRoomType:
            case RoomType.FOOD | RoomType.ITEM:
                self._roomEvent.draw()
