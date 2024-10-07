import pygame
import random

from Config import GeneralConfig
from Config import ActionLogConfig
from Game import SCREEN
from Game import subscribeToEvent
from RoomManager import RoomEvents
from RoomManager import RoomType
from Player import PlayerEvents
from Item import ItemType
from EnemyManager import EnemyEvents
from EnemyManager import EnemyType

class Log:
    fontHeight = 0.0
    positionX = ActionLogConfig.ACTION_LOG_OFFSET_X

    def __init__(self, text: pygame.surface, prevPositionY: float):
        self._text = text
        self._positionY = prevPositionY + ActionLogConfig.ACTION_LOG_OFFSET_Y
        if prevPositionY != 0:
            self._positionY += Log.fontHeight

    @property
    def text(self) -> str:
        return self._text

    @property
    def position(self) -> pygame.Vector2:
        return pygame.Vector2(Log.positionX, self._positionY)

class ActionLogManager:
    def __init__(self):
        self._currentText: str = ''
        self._logs: List[Log] = []
        self._font: pygame.font.Font = pygame.font.SysFont(GeneralConfig.FONT, ActionLogConfig.ACTION_LOG_TEXT_SIZE)
        Log.fontHeight = self._font.get_height()
        self._addLog(ActionLogConfig.GREETING_MESSAGE)
        self._subscribeToEvents()

    def _subscribeToEvents(self):
        subscribeToEvent(RoomEvents.roomGeneratedEventType, self._onRoomEntered)
        subscribeToEvent(PlayerEvents.playerHealthFullEvenType, self._onPlayerHealthFull)
        subscribeToEvent(PlayerEvents.playerHealedEventType, self._onPlayerHealed)
        subscribeToEvent(PlayerEvents.playerTakenItemEventType, self._onItemTaken)
        subscribeToEvent(PlayerEvents.playerUsedItemEventType, self._onItemUsed)
        subscribeToEvent(PlayerEvents.playerHurtEventType, self._onPlayerHurt)
        subscribeToEvent(PlayerEvents.playerDiedEventType, self._onPlayerDied)
        subscribeToEvent(PlayerEvents.playerAttackedEventType, self._onPlayerAttacked)
        subscribeToEvent(PlayerEvents.playerTriedParryEventType, self._onPlayerTriedParry)
        subscribeToEvent(PlayerEvents.playerParriedEventType, self._onPlayerParried)
        subscribeToEvent(PlayerEvents.playerFailedParryEventType, self._onPlayerFailedParry)
        subscribeToEvent(EnemyEvents.enemySpawnedEventType, self._onEnemySpawned)
        subscribeToEvent(EnemyEvents.enemyDefeatedEvenType, self._onEnemyDefeated)
        subscribeToEvent(EnemyEvents.enemyTakenCriticalDamageEventType, self._onCriticalDamage)

    def reset(self):
        self._logs = []
        self._addLog(ActionLogConfig.GREETING_MESSAGE)

    def _addLog(self, message: str):
        self._currentText = ''
        text = self._font.render(message, 1, GeneralConfig.WHITE)
        if len(self._logs) > 0:
            self._logs.append(Log(text, self._logs[-1].position.y))
        else:
            self._logs.append(Log(text, 0))

    def drawLogs(self):
        for log in self._logs:
            SCREEN.blit(log.text, log.position)

    def _removePunctuation(self, string: str) -> str:
        newString = string
        if '_' in newString:
            newString = newString.replace('_', ' ')
        return newString

    def _onRoomEntered(self, roomType: RoomType):
        if roomType is not RoomType.COMBAT:
            message = ActionLogConfig.ROOM_ENTERED_MESSAGE
            match roomType:
                case RoomType.FOOD:
                    message += ' ' + ActionLogConfig.FOOD_ROOM_MESSAGE
                case RoomType.ITEM:
                    message += ' ' + ActionLogConfig.ITEM_ROOM_MESSAGE

            self._addLog(message)

    def _onPlayerHealthFull(self):
        message = ActionLogConfig.FULL_HEALTH_MESSAGE
        self._addLog(message)

    def _onPlayerHealed(self, healAmount: int):
        message = ActionLogConfig.HEAL_MESSAGE.format(healAmount)
        self._addLog(message)

    def _onItemTaken(self, itemType: ItemType):
        name = self._removePunctuation(itemType.name.lower())
        message = ActionLogConfig.ITEM_TAKEN_MESSAGE.format(name)
        self._addLog(message)

    def _onItemUsed(self, itemType: ItemType, power: int):
        name = self._removePunctuation(itemType.name.lower())
        self._currentText += ActionLogConfig.ITEM_USED_MESSAGE.format(name) + ' '

    def _onPlayerHurt(self, damageAmount: int):
        self._currentText += ActionLogConfig.HURT_MESSAGE.format(damageAmount.__abs__())
        self._addLog(self._currentText)

    def _onPlayerDied(self):
        message = ActionLogConfig.DIED_MESSAGE
        self._addLog(message)

    def _onPlayerAttacked(self, damage: int):
        self._currentText += ActionLogConfig.ATTACK_MESSAGE.format(damage) + ' '

    def _onPlayerTriedParry(self):
        self._currentText += ActionLogConfig.TRY_PARRY_MESSAGE + ' '

    def _onPlayerParried(self):
        self._currentText += ActionLogConfig.PARRY_SUCCESS_MESSAGE
        self._addLog(self._currentText)

    def _onPlayerFailedParry(self):
        self._currentText += ActionLogConfig.PARRY_FAIL_MESSAGE
        self._addLog(self._currentText)

    def _onEnemySpawned(self, enemyType: EnemyType):
        name = self._removePunctuation(enemyType.name.lower())
        adjective = random.choice(ActionLogConfig.ENEMY_ADJECTIVES)
        message = ActionLogConfig.ROOM_ENTERED_MESSAGE + ' ' + ActionLogConfig.ENEMY_SPAWNED_MESSAGE.format(adjective, name)
        self._addLog(message)

    def _onEnemyDefeated(self, enemyType: EnemyType):
        name = self._removePunctuation(enemyType.name.lower())
        self._currentText += ActionLogConfig.ENEMY_DEFEATED_MESSAGE.format(name)
        self._addLog(self._currentText)

    def _onCriticalDamage(self, damage: int):
        self._currentText += ActionLogConfig.ENEMY_CRITICAL_DAMAGE.format(damage) + ' '