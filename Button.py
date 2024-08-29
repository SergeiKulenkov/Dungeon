import pygame
import Config
from enum import Enum

class ButtonType(Enum):
    START = 1
    ATTACK = 2
    ITEM = 3
    PARRY = 4
    EVADE = 5

def getTextFont(type):
    font = None
    match type:
        case ButtonType.START:
            font = pygame.font.SysFont(Config.FONT, Config.START_BUTTON_TEXT_SIZE)
        case _:
            font = pygame.font.SysFont(Config.FONT, Config.BUTTON_TEXT_SIZE)

    return font


def getTextFromType(type):
    text = ''
    match type:
        case ButtonType.START:
            text = Config.START_BUTTON_TEXT
        case ButtonType.ATTACK:
            text = Config.ATTACK_BUTTON_TEXT
        case ButtonType.ITEM:
            text = Config.ITEM_BUTTON_TEXT
        case ButtonType.PARRY:
            text = Config.PARRY_BUTTON_TEXT
        case ButtonType.EVADE:
            text = Config.EVADE_BUTTON_TEXT
        case _:
            text = ''

    return text

class Outline:
    def __init__(self, colour, thickness):
        self.colour = colour
        self.thickness = thickness

    def draw(self, surface, x, y, buttonWidth, buttonHeight):
        pygame.draw.rect(surface, self.colour, (x - self.thickness, y - self.thickness,
                                                buttonWidth + self.thickness * 2, buttonHeight + self.thickness * 2))
class Button:
    def __init__(self, colour, x, y, width, height, type):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type

        text = getTextFromType(self.type)
        if text != '':
            font = getTextFont(self.type)
            if font is not None:
                self.text = font.render(text, 1, Config.BLACK)

        self.hasOutline = False
        self.outline = Outline(Config.GREEN, Config.BUTTON_OUTLINE_THICKNESS)
        self.offsetX = self.width / 2 - self.text.get_width() / 2
        self.offsetY = self.height / 2 - self.text.get_height() / 2

    def draw(self, surface):
        if self.hasOutline and self.outline is not None:
            self.outline.draw(surface, self.x, self.y, self.width, self.height)

        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))
        surface.blit(self.text, (self.x + self.offsetX, self.y + self.offsetY))

    def isOver(self, position: pygame.math.Vector2):
        if position.x > self.x and position.x < self.x + self.width:
            if position.y > self.y and position.y < self.y + self.height:
                return True

        return False

    def addOutline(self):
        self.hasOutline = True

    def removeOutline(self):
        self.hasOutline = False
