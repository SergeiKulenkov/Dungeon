import pygame
from Game.Game import SCREEN
from Game.Config import GeneralConfig
from Game.Config import ButtonsConfig
from Button.ButtonManager import ButtonType

class Outline:
    def __init__(self, colour: pygame.color, thickness: float):
        self.colour = colour
        self.thickness = thickness

    def draw(self, x: float, y: float, buttonWidth: float, buttonHeight: float):
        pygame.draw.rect(SCREEN, self.colour, (x - self.thickness, y - self.thickness,
                                                buttonWidth + self.thickness * 2, buttonHeight + self.thickness * 2))
class Button:
    def __init__(self, colour: pygame.color, x: float, y: float, width: float, height: float, type: ButtonType):
        self.colour = colour
        self._position = pygame.math.Vector2(x, y)
        self._width = width
        self._height = height
        self._type = type
        self._text: pygame.Surface = None

        text = Button.getTextFromType(self._type)
        if text != '':
            font = Button.getTextFont(self._type)
            if font is not None:
                self._text = font.render(text, 1, GeneralConfig.BLACK)

        self.hasOutline = False
        self.outline = Outline(GeneralConfig.GREEN, ButtonsConfig.BUTTON_OUTLINE_THICKNESS)
        self.offsetX = self._width / 2 - self._text.get_width() / 2
        self.offsetY = self._height / 2 - self._text.get_height() / 2

    @property
    def type(self) -> ButtonType:
        return self._type

    def draw(self):
        if self.hasOutline and self.outline is not None:
            self.outline.draw(self._position.x, self._position.y, self._width, self._height)

        pygame.draw.rect(SCREEN, self.colour, (self._position.x, self._position.y, self._width, self._height))
        SCREEN.blit(self._text, (self._position.x + self.offsetX, self._position.y + self.offsetY))

    def checkHover(self, position: pygame.math.Vector2) -> bool:
        hover = False
        if position.x > self._position.x and position.x < self._position.x + self._width:
            if position.y > self._position.y and position.y < self._position.y + self._height:
                hover = True

        return hover

    def addOutline(self):
        self.hasOutline = True

    def removeOutline(self):
        self.hasOutline = False

    @staticmethod
    def getTextFont(type: ButtonType) -> pygame.font.Font:
        font = None
        match type:
            case ButtonType.START | ButtonType.QUIT:
                font = pygame.font.SysFont(GeneralConfig.FONT, ButtonsConfig.MENU_BUTTON_TEXT_SIZE)
            case _:
                font = pygame.font.SysFont(GeneralConfig.FONT, ButtonsConfig.BUTTON_TEXT_SIZE)

        return font

    @staticmethod
    def getTextFromType(type: ButtonType) -> str:
        text = ''
        match type:
            case ButtonType.START:
                text = ButtonsConfig.START_BUTTON_TEXT
            case ButtonType.LEAVE:
                text = ButtonsConfig.LEAVE_BUTTON_TEXT
            case ButtonType.EAT:
                text = ButtonsConfig.EAT_BUTTON_TEXT
            case ButtonType.ATTACK:
                text = ButtonsConfig.ATTACK_BUTTON_TEXT
            case ButtonType.PARRY:
                text = ButtonsConfig.PARRY_BUTTON_TEXT
            case ButtonType.TAKE_ITEM:
                text = ButtonsConfig.TAKE_ITEM_BUTTON_TEXT
            case ButtonType.USE_ITEM:
                text = ButtonsConfig.USE_ITEM_BUTTON_TEXT
            case ButtonType.QUIT:
                text = ButtonsConfig.QUIT_BUTTON_TEXT
            case _:
                text = ''

        return text
