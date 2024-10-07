from enum import Enum
import random
import pygame

class PlayerEvents:
    playerAttackedEventType = pygame.event.custom_type()
    playerTriedParryEventType = pygame.event.custom_type()
    playerParriedEventType = pygame.event.custom_type()
    playerFailedParryEventType = pygame.event.custom_type()
    playerHealthFullEvenType = pygame.event.custom_type()
    playerHealedEventType = pygame.event.custom_type()
    playerTakenItemEventType = pygame.event.custom_type()
    playerUsedItemEventType = pygame.event.custom_type()
    playerHurtEventType = pygame.event.custom_type()
    playerDiedEventType = pygame.event.custom_type()
    enemyDefeatedEventType = pygame.event.custom_type()

def isPlayerItemAvailable() -> bool:
    return Player.hasItem

from Game import subscribeToEvent
from Config import CharacterConfig
from Character import Character
from EnemyManager import EnemyEvents
from EnemyManager import EnemyType
from RoomManager import RoomEvents
from ButtonManager import ButtonEvents
from ButtonManager import ButtonType
from Item import ItemType
from Item import Item

class ScoreType(Enum):
    ENEMY = 0
    TREASURE = 1
    ITEM = 2

class Score:
    type: ScoreType = ScoreType.ENEMY
    value = 0

    def __init__(self, type: ScoreType, value: int):
        self.type = type
        self.value = value

class Player:
    hasItem = False

    def __init__(self):
        self._character = Character()
        self._triedParry = False
        self._score: list[Score] = []

        self._attackedEvent = pygame.event.Event(PlayerEvents.playerAttackedEventType, { CharacterConfig.ATTACK_VALUE : 0 })
        self._triedParryEvent = pygame.event.Event(PlayerEvents.playerTriedParryEventType)
        self._parriedEvent = pygame.event.Event(PlayerEvents.playerParriedEventType)
        self._failedParryEvent = pygame.event.Event(PlayerEvents.playerFailedParryEventType)
        self._healthFullEvent = pygame.event.Event(PlayerEvents.playerHealthFullEvenType)
        self._healedEvent = pygame.event.Event(PlayerEvents.playerHealedEventType, { CharacterConfig.HP_CHANGE_VALUE : 0 })
        self._takenItemEvent = pygame.event.Event(PlayerEvents.playerTakenItemEventType, { CharacterConfig.ITEM_TYPE_VALUE : 0 })
        self._usedItemEvent = pygame.event.Event(PlayerEvents.playerUsedItemEventType,{ CharacterConfig.ITEM_TYPE_VALUE: 0 })
        self._hurtEvent = pygame.event.Event(PlayerEvents.playerHurtEventType, { CharacterConfig.HP_CHANGE_VALUE : 0 })
        self._diedEvent = pygame.event.Event(PlayerEvents.playerDiedEventType)
        self._enemyDefeatedEvent = pygame.event.Event(PlayerEvents.enemyDefeatedEventType)

        subscribeToEvent(RoomEvents.foodEatenEventType, self._onFoodEaten)
        subscribeToEvent(RoomEvents.itemTakenEventType, self._onItemTaken)
        subscribeToEvent(ButtonEvents.buttonPressedEventType, self._handleCombatButtons)
        subscribeToEvent(EnemyEvents.enemyAttackedEventType, self._takeDamage)
        subscribeToEvent(EnemyEvents.enemyDefeatedEvenType, self._onEnemyDefeated)

    def reset(self):
        self._character = Character()
        self._score: list[Score] = []
        Player.hasItem = False

    def _onFoodEaten(self, hp: int):
        if self._character.changeHealth(hp):
            self._healedEvent.dict[CharacterConfig.HP_CHANGE_VALUE] = hp
            pygame.event.post(self._healedEvent)
        else:
            pygame.event.post(self._healthFullEvent)

    def _onItemTaken(self, item: Item):
        if item.isSingleUse:
            self._character.changeItem(item)
            Player.hasItem = True
        else:
            match item.type:
                case ItemType.AXE:
                    self._character.changeDamage(item.power)
                case ItemType.TREASURE:
                    score = random.randint(CharacterConfig.MIN_TREASURE_SCORE, CharacterConfig.MAX_TREASURE_SCORE)
                    self._score.append(Score(ScoreType.TREASURE, score))

        self._takenItemEvent.dict[CharacterConfig.ITEM_TYPE_VALUE] = item.type
        pygame.event.post(self._takenItemEvent)

    def _useItem(self):
        self._usedItemEvent.dict[CharacterConfig.ITEM_TYPE_VALUE] = self._character.itemType
        self._usedItemEvent.dict[CharacterConfig.ITEM_POWER_VALUE] = self._character.itemPower
        pygame.event.post(self._usedItemEvent)
        self._character.removeItem()
        Player.hasItem = False

    def _takeDamage(self, damage: int):
        takingDamage = not self._triedParry
        if self._triedParry:
            chance = random.randint(0, CharacterConfig.MAX_PARRY_LUCK)
            if self._character.luck >= chance:
                pygame.event.post(self._parriedEvent)
                self._attack(CharacterConfig.PARRY_DAMAGE_MULTIPLIER)
            else:
                takingDamage = True
                pygame.event.post(self._failedParryEvent)

        if takingDamage:
            if self._character.changeHealth(damage):
                if not self._character.isAlive():
                    pygame.event.post(self._diedEvent)
                else:
                    self._hurtEvent.dict[CharacterConfig.HP_CHANGE_VALUE] = damage
                    pygame.event.post(self._hurtEvent)

    def _handleCombatButtons(self, buttonType: ButtonType):
        match buttonType:
            case ButtonType.ATTACK:
                self._attack()
            case ButtonType.PARRY:
                self._triedParry = True
                pygame.event.post(self._triedParryEvent)
            case ButtonType.USE_ITEM:
                self._useItem()
            case ButtonType.PARRY:
                pass

    def _attack(self, damageMultiplier: float=1):
        self._attackedEvent.dict[CharacterConfig.ATTACK_VALUE] = self._character.damage * damageMultiplier
        pygame.event.post(self._attackedEvent)

    def _onEnemyDefeated(self, type: EnemyType):
        value = CharacterConfig.ENEMY_SCORE[type.name]
        self._score.append(Score(ScoreType.ENEMY, value))
        pygame.event.post(self._enemyDefeatedEvent)

    def getScoreText(self) -> list[str]:
        scoreTexts: list[str] = [''] * len(ScoreType)
        values: list[int] = [0] * len(ScoreType)

        if Player.hasItem:
            if self._character.itemType is ItemType.MAGIC_SCROLL:
                self._score.append(Score(ScoreType.ITEM, CharacterConfig.MAGIC_SCROLL_SCORE))
            else:
                self._score.append(Score(ScoreType.ITEM, CharacterConfig.ITEM_SCORE))

        for score in self._score:
            values[score.type.value] += score.value

        for scoreType in ScoreType:
            match scoreType:
                case ScoreType.ENEMY:
                    scoreTexts[scoreType.value] = CharacterConfig.SCORE_ENEMY_TEXT
                case ScoreType.TREASURE:
                    scoreTexts[scoreType.value] = CharacterConfig.SCORE_TREASURE_TEXT
                case ScoreType.ITEM:
                    scoreTexts[scoreType.value] = CharacterConfig.SCORE_ITEM_TEXT
            scoreTexts[scoreType.value] += ' ' + str(values[scoreType.value])

        return scoreTexts

    def draw(self):
        self._character.drawStats()
        self._character.drawItem()