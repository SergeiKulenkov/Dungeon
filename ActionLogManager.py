import pygame
import Config
from Game import SCREEN


class ActionLogManager:
    def __init__(self):
        self.logs = []
        self.font = pygame.font.SysFont(Config.FONT, Config.ACTION_LOG_TEXT_SIZE)

        text = self.font.render(Config.GREETING_MESSAGE, 1, Config.WHITE)
        self.logs.append(text)

    def onRoomEntered(self):
        text = self.font.render(Config.ROOM_ENTERED_MESSAGE, 1, Config.WHITE)
        self.logs.append(text)

    def drawLogs(self):
        positionX = Config.ACTION_LOG_OFFSET_X
        positionY = Config.ACTION_LOG_OFFSET_Y
        for log in self.logs:
            SCREEN.blit(log, (positionX, positionY))
            positionY += self.font.get_height() + Config.ACTION_LOG_OFFSET_Y