import pygame
import Config
from Game import SCREEN
from Game import DOOR_POSITION_X
from Game import DOOR_POSITION_Y
from Game import subscribe
from Game import leftMouseClickEventType
from Game import mouseMotionEventType
from Game import gameStartedEventType
from Button import Button
from Button import ButtonType

startButtonPressedEventType = pygame.event.custom_type()
startButtonPressedEvent = pygame.event.Event(startButtonPressedEventType)

class ButtonManager:
    def __init__(self):
        self.buttons = []

        positionX = DOOR_POSITION_X + Config.DOOR_WIDTH / 2 - Config.START_BUTTON_WIDTH / 2
        positionY = DOOR_POSITION_Y + Config.DOOR_HEIGHT / 2 - Config.START_BUTTON_HEIGHT / 2
        startButton = Button(Config.ORANGE, positionX, positionY, Config.START_BUTTON_WIDTH, Config.START_BUTTON_HEIGHT, ButtonType.START)
        self.buttons.append(startButton)

        # sub to mouse events
        subscribe(leftMouseClickEventType, self.handleLeftMouseClick)
        subscribe(mouseMotionEventType, self.handleMouseHover)
        subscribe(gameStartedEventType, self.onGameStarted)

    def drawButtons(self):
        for button in self.buttons:
            button.draw(SCREEN)

    def handleLeftMouseClick(self, mousePosition: pygame.math.Vector2):
        for button in self.buttons:
            if button.isOver(mousePosition):
                button.colour = Config.GREEN

                if button.type is ButtonType.START:
                    pygame.event.post(startButtonPressedEvent)
                break

    def handleMouseHover(self, mousePosition: pygame.math.Vector2):
        for button in self.buttons:
            if button.isOver(mousePosition):
                button.addOutline()
            else:
                button.removeOutline()

    def removeStartButton(self):
        for button in self.buttons:
            if button.type is ButtonType.START:
                self.buttons.remove(button)

    def onGameStarted(self):
        self.removeStartButton()