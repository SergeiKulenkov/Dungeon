from enum import Enum
from typing import Any
import os.path

import pygame
from Config import GeneralConfig
from Config import GameConfig
from Config import EnemyConfig
from Config import RoomConfig

SCREEN = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
BORDER_ACTION = pygame.Rect(SCREEN.get_width() * GameConfig.BORDER_ACTION_OFFSET_X_PERCENT, 0, GameConfig.BORDER_WIDTH, SCREEN.get_height() - GameConfig.BORDER_STATS_OFFSET_Y)
BORDER_STATS = pygame.Rect(0, SCREEN.get_height() - GameConfig.BORDER_STATS_OFFSET_Y, SCREEN.get_width(), GameConfig.BORDER_WIDTH)

DOOR_POSITION_X = BORDER_ACTION.x + (SCREEN.get_width() - BORDER_ACTION.x) / 2 - GeneralConfig.DOOR_WIDTH / 2
DOOR_POSITION_Y = BORDER_STATS.y / 2 - GeneralConfig.DOOR_HEIGHT / 2

class GameEvents:
    leftMouseClickEventType = pygame.event.custom_type()
    mouseMotionEventType = pygame.event.custom_type()
    gameStartedEventType = pygame.event.custom_type()
    roomEnteredEventType = pygame.event.custom_type()
    gameFinishStartedEventType = pygame.event.custom_type()
    gameFinishedEventType = pygame.event.custom_type()

def subscribeToEvent(eventType: pygame.event.EventType, subscriber: Any):
    Game.eventHandler.subscribe(eventType, subscriber)

def unSubscribeFromEvent(eventType: pygame.event.EventType, subscriber: Any):
    Game.eventHandler.unsubscribe(eventType, subscriber)

from EventHandler import EventHandler
from Player import Player
from Player import PlayerEvents
from Item import ItemType
from ButtonManager import ButtonManager
from ButtonManager import ButtonType
from ButtonManager import ButtonEvents
from RoomManager import RoomManager
from EnemyManager import EnemyManager
from EnemyManager import EnemyEvents
from ActionLogManager import ActionLogManager

class DelayType(Enum):
    NONE = 0
    START = 1
    NEXT_ROOM = 2
    ENEMY_ATTACK = 3
    FINISH = 4

class GameState(Enum):
    NONE = 0
    STARTED = 1
    FINISHED = 2
    RESTARTED = 3

class Game:
    eventHandler: EventHandler = None
    DOOR_IMAGE = pygame.image.load(os.path.join(GeneralConfig.IMAGES_PATH, GameConfig.DOOR_IMAGE))
    DOOR = pygame.transform.scale(DOOR_IMAGE, (GeneralConfig.DOOR_WIDTH, GeneralConfig.DOOR_HEIGHT))

    def __init__(self):
        self._gameClock = pygame.time.Clock()
        self._deltaTime = 0.0
        self._gameState = GameState.NONE
        self._isRunning = True
        self._mousePosition = pygame.math.Vector2()

        self._delayTimer = 0.0
        self._delayType = DelayType.NONE
        self._roomCount = 0
        self._finishText: pygame.Surface = None
        self._scoreText: list[str] = []

        Game.eventHandler = EventHandler()
        self._buttonManager = ButtonManager()
        self._roomManager: RoomManager = None
        self._enemyManager: EnemyManager = None
        self._actionLogManager: ActionLogManager = None
        self._player: Player = None

        self._leftMouseClickEvent = pygame.event.Event(GameEvents.leftMouseClickEventType, { GameConfig.MOUSE_POSITION_VALUE : None })
        self._mouseMotionEvent = pygame.event.Event(GameEvents.mouseMotionEventType, { GameConfig.MOUSE_POSITION_VALUE : None })
        self._gameStartedEvent = pygame.event.Event(GameEvents.gameStartedEventType)
        self._roomEnteredEvent = pygame.event.Event(GameEvents.roomEnteredEventType)
        self._gameFinishStartedEvent = pygame.event.Event(GameEvents.gameFinishStartedEventType)
        self._gameFinishedEvent = pygame.event.Event(GameEvents.gameFinishedEventType)

        self._subscribeToEvents()

    def _subscribeToEvents(self):
        subscribeToEvent(pygame.QUIT, self._stopGame)
        subscribeToEvent(pygame.MOUSEBUTTONDOWN, self._handleMouseClick)
        subscribeToEvent(pygame.MOUSEMOTION, self._handleMouseMotion)
        subscribeToEvent(ButtonEvents.buttonPressedEventType, self._delayButtonPress)
        subscribeToEvent(PlayerEvents.playerTakenItemEventType, self._onItemTaken)
        subscribeToEvent(PlayerEvents.enemyDefeatedEventType, self._delayNextRoom)
        subscribeToEvent(PlayerEvents.playerDiedEventType, self._startGameOver)
        subscribeToEvent(EnemyEvents.enemyStartedAttackEvenType, self._startEnemyAttack)

    def _drawWindow(self):
        SCREEN.fill(GeneralConfig.BLACK)
        # the door is always there
        SCREEN.blit(Game.DOOR, (DOOR_POSITION_X, DOOR_POSITION_Y))

        if self._gameState == GameState.STARTED:
            pygame.draw.rect(SCREEN, GeneralConfig.GREY, BORDER_ACTION)
            pygame.draw.rect(SCREEN, GeneralConfig.GREY, BORDER_STATS)
            self._player.draw()
            self._roomManager.drawRoom()
            self._actionLogManager.drawLogs()
            self._enemyManager.draw()
        elif self._gameState == GameState.FINISHED:
            self._player.draw()
            self._actionLogManager.drawLogs()

            positionY = SCREEN.get_height() * GameConfig.FINISH_TEXT_OFFSET_Y
            SCREEN.blit(self._finishText, (SCREEN.get_width() / 2 - self._finishText.get_width() / 2,
                                           positionY - self._finishText.get_height() / 2))

            positionY += self._finishText.get_height() / 2 + GameConfig.SCORE_TEXT_OFFSET
            for score in self._scoreText:
                SCREEN.blit(score, (SCREEN.get_width() / 2 - score.get_width() / 2, positionY))
                positionY += GameConfig.SCORE_TEXT_OFFSET + score.get_height()

        self._buttonManager.drawButtons()
        pygame.display.update()

    def _startGame(self):
        if self._gameState is not GameState.RESTARTED:
            self._roomManager = RoomManager()
            self._enemyManager = EnemyManager()
            self._actionLogManager = ActionLogManager()
            self._player = Player()

        self._delayTimer = 0.0
        self._gameState = GameState.STARTED
        self._roomCount += 1
        pygame.event.post(self._gameStartedEvent)

    def _reset(self):
        self._roomCount = 0
        self._scoreText = []
        self._buttonManager.reset()
        self._roomManager.reset()
        self._enemyManager.reset()
        self._actionLogManager.reset()
        self._player.reset()

    def _stopGame(self):
        self._isRunning = False

    def _handleMouseClick(self, *mouseClickValues):
        self._mousePosition = pygame.math.Vector2(pygame.mouse.get_pos())
        self._leftMouseClickEvent.dict[GameConfig.MOUSE_POSITION_VALUE] = self._mousePosition
        pygame.event.post(self._leftMouseClickEvent)

    def _handleMouseMotion(self, *mouseMotionValues):
        self._mousePosition = pygame.math.Vector2(pygame.mouse.get_pos())
        self._mouseMotionEvent.dict[GameConfig.MOUSE_POSITION_VALUE] = self._mousePosition
        pygame.event.post(self._mouseMotionEvent)

    def _delayButtonPress(self, buttonType: ButtonType):
        match buttonType:
            case ButtonType.START:
                if self._gameState is GameState.FINISHED:
                    self._reset()
                    self._gameState = GameState.RESTARTED
                self._delayType = DelayType.START
                self._delayTimer = GameConfig.GAME_START_DELAY
            case ButtonType.EAT | ButtonType.LEAVE:
                self._delayNextRoom()
            case ButtonType.QUIT:
                self._stopGame()

    def _delayNextRoom(self):
            if self._roomCount < GameConfig.MAX_NUMBER_OF_ROOMS:
                self._delayType = DelayType.NEXT_ROOM
                self._delayTimer = RoomConfig.NEXT_ROOM_DELAY
            else:
                if self._gameState is not GameState.FINISHED:
                    self._finish(False)

    def _onItemTaken(self, itemType: ItemType):
        self._delayNextRoom()

    def _enterNextRoom(self):
        self._delayTimer = 0.0
        self._roomCount += 1
        pygame.event.post(self._roomEnteredEvent)

    def _startEnemyAttack(self):
        self._delayType = DelayType.ENEMY_ATTACK
        self._delayTimer = EnemyConfig.ENEMY_ATTACK_DELAY

    def _finishEnemyAttack(self):
        self._delayTimer = 0.0
        self._enemyManager.finishAttack()

    def _startGameOver(self):
        self._finish(True)

    def _finish(self, isGameOver: bool):
        self._gameState = GameState.FINISHED
        self._delayType = DelayType.FINISH
        self._delayTimer = GameConfig.FINISH_DELAY
        text = ''

        if isGameOver:
            text = GameConfig.GAME_OVER_TEXT
        else:
            text = GameConfig.FINISH_TEXT

        font = pygame.font.SysFont(GeneralConfig.FONT, GameConfig.FINISH_TEXT_SIZE)
        self._finishText = font.render(text, 1, GeneralConfig.GREEN)

        font = pygame.font.SysFont(GeneralConfig.FONT, GameConfig.SCORE_TEXT_SIZE)
        self._scoreText.append(font.render(GameConfig.SCORE_TEXT, 1, GeneralConfig.GREEN))
        for score in self._player.getScoreText():
            self._scoreText.append(font.render(score, 1, GeneralConfig.GREEN))

        pygame.event.post(self._gameFinishStartedEvent)

    def run(self):
        while self._isRunning:
            self.eventHandler.dispatchEvents(pygame.event.get())
            self._drawWindow()
            self._update()

    def _update(self):
        self._gameClock.tick(GameConfig.FPS)
        self._deltaTime = self._gameClock.get_time() / 1000

        if self._delayTimer > 0:
            self._delayTimer -= self._deltaTime
        elif self._delayTimer < 0:
            match self._delayType:
                case DelayType.START:
                    self._startGame()
                case DelayType.NEXT_ROOM:
                    self._enterNextRoom()
                case DelayType.ENEMY_ATTACK:
                    self._finishEnemyAttack()
                case DelayType.FINISH:
                    pygame.event.post(self._gameFinishedEvent)
                case DelayType.NONE:
                    pass
            self._delayType = DelayType.NONE