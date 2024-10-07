import pygame
from enum import Enum

from Config import GeneralConfig
from Config import ButtonsConfig
from Game import SCREEN
from Game import DOOR_POSITION_X
from Game import DOOR_POSITION_Y
from Game import subscribeToEvent

class ButtonEvents:
    buttonPressedEventType = pygame.event.custom_type()

class ButtonType(Enum):
    START = 0
    LEAVE = 1
    EAT = 2
    ATTACK = 3
    PARRY = 4
    TAKE_ITEM = 5
    USE_ITEM = 6
    QUIT = 7

from Game import GameEvents
from RoomManager import RoomEvents
from RoomManager import RoomType
from EnemyManager import EnemyEvents
from Player import isPlayerItemAvailable
from Player import PlayerEvents
from Item import ItemType
from Button import Button

class ButtonManager:
    buttonLayouts = { RoomType.FOOD : [ButtonType.EAT, ButtonType.LEAVE],
                      RoomType.COMBAT : [ButtonType.ATTACK, ButtonType.PARRY, ButtonType.USE_ITEM],
                      RoomType.ITEM : [ButtonType.TAKE_ITEM, ButtonType.LEAVE], }
    finishLayout = [ButtonType.START, ButtonType.QUIT]

    def __init__(self):
        self._buttons = []

        positionX = DOOR_POSITION_X + GeneralConfig.DOOR_WIDTH / 2 - ButtonsConfig.MENU_BUTTON_WIDTH / 2
        positionY = DOOR_POSITION_Y + GeneralConfig.DOOR_HEIGHT / 2 - ButtonsConfig.MENU_BUTTON_HEIGHT / 2
        startButton = Button(GeneralConfig.ORANGE, positionX, positionY, ButtonsConfig.MENU_BUTTON_WIDTH, ButtonsConfig.MENU_BUTTON_HEIGHT, ButtonType.START)
        self._buttons.append(startButton)

        self._buttonPressedEvent = pygame.event.Event(ButtonEvents.buttonPressedEventType, { ButtonsConfig.BUTTON_TYPE_VALUE : ButtonType.START })
        self._subscribeToEvents()

    def _subscribeToEvents(self):
        subscribeToEvent(GameEvents.leftMouseClickEventType, self._handleLeftMouseClick)
        subscribeToEvent(GameEvents.mouseMotionEventType, self._handleMouseHover)
        subscribeToEvent(GameEvents.gameStartedEventType, self._onGameStarted)
        subscribeToEvent(GameEvents.gameFinishStartedEventType, self._onGameFinishStarted)
        subscribeToEvent(GameEvents.gameFinishedEventType, self._onGameFinished)
        subscribeToEvent(EnemyEvents.enemyAttackedEventType, self._onEnemyAttacked)
        subscribeToEvent(PlayerEvents.playerUsedItemEventType, self._onItemUsed)

    def reset(self):
        self._buttons = []

    def drawButtons(self):
        for button in self._buttons:
            button.draw()

    def _handleLeftMouseClick(self, mousePosition: pygame.math.Vector2):
        for button in self._buttons:
            if button.checkHover(mousePosition):
                button.colour = GeneralConfig.GREEN
                self._buttonPressedEvent.dict[ButtonsConfig.BUTTON_TYPE_VALUE] = button._type
                pygame.event.post(self._buttonPressedEvent)
                break

    def _handleMouseHover(self, mousePosition: pygame.math.Vector2):
        for button in self._buttons:
            if button.checkHover(mousePosition):
                button.addOutline()
            else:
                button.removeOutline()

    def _removeButton(self, type: ButtonType):
        for button in self._buttons:
            if button.type is type:
                self._buttons.remove(button)
                break

    def _onEnemyAttacked(self, dmaage: int):
        self._resetCombatButtons()

    def _resetCombatButtons(self):
        for button in self._buttons:
            if button.colour is GeneralConfig.GREEN:
                button.colour = GeneralConfig.ORANGE
                break

    def _onGameStarted(self):
        subscribeToEvent(RoomEvents.roomGeneratedEventType, self._onRoomEntered)
        self._removeButton(ButtonType.START)

    def _onGameFinishStarted(self):
        self._buttons.clear()

    def _onGameFinished(self):
        positionX = DOOR_POSITION_X + GeneralConfig.DOOR_WIDTH / 2 - ButtonsConfig.MENU_BUTTON_WIDTH / 2
        positionY = DOOR_POSITION_Y + GeneralConfig.DOOR_HEIGHT / 2 - ButtonsConfig.MENU_BUTTON_HEIGHT / 2 * len(ButtonManager.finishLayout)
        button = None

        for buttonType in ButtonManager.finishLayout:
            button = Button(GeneralConfig.ORANGE, positionX, positionY, ButtonsConfig.MENU_BUTTON_WIDTH, ButtonsConfig.MENU_BUTTON_HEIGHT, buttonType)
            self._buttons.append(button)
            positionY += ButtonsConfig.MENU_BUTTON_HEIGHT + ButtonsConfig.BUTTON_OFFSET_Y

    def _onItemUsed(self, type: ItemType, power: int):
        self._removeButton(ButtonType.USE_ITEM)

    def _onRoomEntered(self, roomType: RoomType):
        self._buttons.clear()
        buttonOffsetX = (GeneralConfig.DOOR_WIDTH - ButtonsConfig.BUTTON_WIDTH * ButtonsConfig.NUMBER_OF_BUTTONS_IN_ROW) / (ButtonsConfig.NUMBER_OF_BUTTONS_IN_ROW + 1)
        positionX = DOOR_POSITION_X + buttonOffsetX
        positionY = DOOR_POSITION_Y + GeneralConfig.DOOR_HEIGHT + ButtonsConfig.BUTTON_OFFSET_FROM_DOOR_Y
        buttonCount = 0
        button = None

        for buttonType in ButtonManager.buttonLayouts[RoomType(roomType)]:
            if buttonType is ButtonType.USE_ITEM and not isPlayerItemAvailable():
                break

            button = Button(GeneralConfig.ORANGE, positionX, positionY, ButtonsConfig.BUTTON_WIDTH, ButtonsConfig.BUTTON_HEIGHT, buttonType)
            positionX += ButtonsConfig.BUTTON_WIDTH + buttonOffsetX
            if buttonCount % ButtonsConfig.NUMBER_OF_BUTTONS_IN_ROW == 1:
                positionX = DOOR_POSITION_X + buttonOffsetX
                positionY += ButtonsConfig.BUTTON_HEIGHT + ButtonsConfig.BUTTON_OFFSET_Y

            self._buttons.append(button)
            buttonCount += 1