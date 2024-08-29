from enum import Enum
from typing import Any
from typing import Dict
import os.path
import Config
import pygame
from EventHandler import EventHandler

SCREEN = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
BORDER_ACTION = pygame.Rect(SCREEN.get_width() * Config.BORDER_ACTION_OFFSET_X_PERCENT, 0, Config.BORDER_WIDTH, SCREEN.get_height() - Config.BORDER_STATS_OFFSET_Y)
BORDER_STATS = pygame.Rect(0, SCREEN.get_height() - Config.BORDER_STATS_OFFSET_Y, SCREEN.get_width(), Config.BORDER_WIDTH)

DOOR_IMAGE = pygame.image.load(os.path.join(Config.IMAGES_PATH, Config.DOOR_IMAGE))
DOOR = pygame.transform.scale(DOOR_IMAGE, (Config.DOOR_WIDTH, Config.DOOR_HEIGHT))
DOOR_POSITION_X = BORDER_ACTION.x + (SCREEN.get_width() - BORDER_ACTION.x) / 2 - Config.DOOR_WIDTH / 2
DOOR_POSITION_Y = BORDER_STATS.y / 2 - Config.DOOR_HEIGHT / 2

leftMouseClickEventType = pygame.event.custom_type()
mouseMotionEventType = pygame.event.custom_type()
gameStartedEventType = pygame.event.custom_type()

def subscribe(eventType: pygame.event.EventType, subscriber: Any):
    Game.eventHandler.subscribe(eventType, subscriber)

from Button import Button
from Player import Player
from Player import CharacterType
from ButtonManager import ButtonManager
from ButtonManager import startButtonPressedEventType
from RoomManager import RoomManager

class Game:
    eventHandler = EventHandler()

    def __init__(self):
        self.gameClock = pygame.time.Clock()
        self.deltaTime = 0.0
        self.mousePosition = pygame.math.Vector2()
        self.isStarted = False
        self.isRunning = True
        self.startDelayTimer = 0.0

        # remove from class variables??
        self.player = None
        self.buttonManager = ButtonManager()
        self.roomManager = RoomManager()

        self.leftMouseClickEvent = pygame.event.Event(leftMouseClickEventType)
        self.mouseMotionEvent = pygame.event.Event(mouseMotionEventType)
        self.gameStartedEvent = pygame.event.Event(gameStartedEventType)
        subscribe(pygame.QUIT, self.stopGame)
        subscribe(pygame.MOUSEBUTTONDOWN, self.handleMouseClick)
        subscribe(pygame.MOUSEMOTION, self.handleMouseMotion)
        subscribe(startButtonPressedEventType, self.handleStartButtonPress)

    def drawWindow(self):
        SCREEN.fill(Config.BLACK)
        # the door is always there
        SCREEN.blit(DOOR, (DOOR_POSITION_X, DOOR_POSITION_Y))

        if self.isStarted:
            pygame.draw.rect(SCREEN, Config.GREY, BORDER_ACTION)
            pygame.draw.rect(SCREEN, Config.GREY, BORDER_STATS)
            self.player.draw()
            self.roomManager.drawRoom()

        self.buttonManager.drawButtons()

        pygame.display.update()

    def handleStartButtonPress(self):
        self.startDelayTimer = Config.GAME_START_DELAY

    def startGame(self):
        self.player = Player(CharacterType.DEFAULT)
        self.startDelayTimer = 0.0
        self.isStarted = True
        pygame.event.post(self.gameStartedEvent)

    def stopGame(self):
        self.isRunning = False

    def handleMouseClick(self, *args):
        self.mousePosition = pygame.math.Vector2(pygame.mouse.get_pos())
        # add to Config or local const
        self.leftMouseClickEvent.dict['mousePos'] = self.mousePosition
        pygame.event.post(self.leftMouseClickEvent)

    def handleMouseMotion(self, *args):
        self.mousePosition = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mouseMotionEvent.dict['mousePos'] = self.mousePosition
        pygame.event.post(self.mouseMotionEvent)

    def run(self):
        while self.isRunning:
            self.eventHandler.dispatchEvents(pygame.event.get())

            self.drawWindow()
            self.gameClock.tick(Config.FPS)

            if self.startDelayTimer > 0:
                self.startDelayTimer -= self.gameClock.get_time() / 1000
            elif self.startDelayTimer < 0:
                self.startGame()