import pygame
import random
import math
from enum import Enum

class EnemyEvents():
    enemySpawnedEventType = pygame.event.custom_type()
    enemyStartedAttackEvenType = pygame.event.custom_type()
    enemyAttackedEventType = pygame.event.custom_type()
    enemyDefeatedEvenType = pygame.event.custom_type()
    enemyTakenCriticalDamageEventType = pygame.event.custom_type()

from Game.Config import EnemyConfig
from Game.Game import subscribeToEvent
from Room.RoomManager import RoomEvents
from Room.RoomManager import RoomType
from Player.Player import PlayerEvents
from Player.Item import ItemType

class EnemyType(Enum):
    SKELETON = 0
    GOBLIN = 1
    ORC = 2
    SPIDER = 3

from Enemy.Enemy import Enemy

class EnemyManager:
    def __init__(self):
        self._currentEnemy: Enemy = None
        self._easyEnemiesInRow = 0
        self._easyEnemyCooldown = 0
        self._hardEnemyCooldown = 0
        self._startedAttack = False

        self._enemySpawnedEvent = pygame.event.Event(EnemyEvents.enemySpawnedEventType, { EnemyConfig.TYPE_VALUE : None })
        self._enemyStartedAttackEvent = pygame.event.Event(EnemyEvents.enemyStartedAttackEvenType)
        self._enemyAttackedEvent = pygame.event.Event(EnemyEvents.enemyAttackedEventType, { EnemyConfig.DAMAGE_VALUE : 0 })
        self._enemyDefeatedEvent = pygame.event.Event(EnemyEvents.enemyDefeatedEvenType, { EnemyConfig.TYPE_VALUE : None })
        self._enemyTakenCriticalDamageEvent = pygame.event.Event(EnemyEvents.enemyTakenCriticalDamageEventType, { EnemyConfig.CRITICAL_DAMAGE_VALUE : 0 })

        subscribeToEvent(RoomEvents.roomGeneratedEventType, self._onRoomEntered)
        subscribeToEvent(PlayerEvents.playerAttackedEventType, self._onPlayerAttacked)
        subscribeToEvent(PlayerEvents.playerTriedParryEventType, self._onPlayerTriedParry)
        subscribeToEvent(PlayerEvents.playerUsedItemEventType, self._onItemUsed)

    def reset(self):
        self._easyEnemiesInRow = 0
        self._easyEnemyCooldown = 0
        self._hardEnemyCooldown = 0

    def _spawnEnemy(self):
        enemyType = EnemyType.SKELETON
        randomProbability = random.random()
        enemyProbabilities = list(EnemyConfig.ENEMIES_PROBABILITIES.items())

        if self._easyEnemyCooldown > 0:
            enemyProbabilities.pop(0)
        if self._hardEnemyCooldown > 0:
            enemyProbabilities.pop()

        for name, probability in enemyProbabilities:
            randomProbability -= probability
            if randomProbability <= 0:
                enemyType = EnemyType.__getitem__(name)
                break

        if self._easyEnemyCooldown > 0:
            self._easyEnemyCooldown -= 1
            if self._easyEnemyCooldown <= 0:
                self._easyEnemiesInRow = 0
        elif enemyType is EnemyType.SKELETON:
            self._easyEnemiesInRow += 1
            if self._easyEnemiesInRow >= EnemyConfig.EASY_ENEMIES_IN_A_ROW:
                self._easyEnemyCooldown = EnemyConfig.EASY_ENEMY_COOLDOWN


        if self._hardEnemyCooldown > 0:
            self._hardEnemyCooldown -= 1
        elif enemyType is EnemyType.SPIDER:
            self._hardEnemyCooldown = EnemyConfig.HARD_ENEMY_COOLDOWN

        self._currentEnemy = Enemy(enemyType)

    def _onRoomEntered(self, roomType: RoomType):
        if roomType is RoomType.COMBAT:
            self._spawnEnemy()
            self._enemySpawnedEvent.dict[EnemyConfig.TYPE_VALUE] = self._currentEnemy.type
            pygame.event.post(self._enemySpawnedEvent)

    def _checkDefeat(self):
        if not self._currentEnemy.isAlive():
            self._enemyDefeatedEvent.dict[EnemyConfig.TYPE_VALUE] = self._currentEnemy.type
            pygame.event.post(self._enemyDefeatedEvent)
            self._currentEnemy = None
        else:
            self._startedAttack = True
            pygame.event.post(self._enemyStartedAttackEvent)

    def _onPlayerAttacked(self, damage: int):
        if self._currentEnemy is not None:
            self._currentEnemy.takeDamage(damage)
            self._checkDefeat()

    def _onPlayerTriedParry(self):
        if self._currentEnemy is not None:
            self._startedAttack = True
            pygame.event.post(self._enemyStartedAttackEvent)

    def _onItemUsed(self, itemType: ItemType, power: int):
        if self._currentEnemy is not None:
            damage = power
            itemEnemyCombo = (itemType.name, self._currentEnemy.type.name)

            for combo, multiplier in EnemyConfig.ITEM_INTERACTIONS.items():
                if itemEnemyCombo == combo:
                    damage = math.ceil(damage * multiplier)
                    if multiplier > 1:
                        self._enemyTakenCriticalDamageEvent.dict[EnemyConfig.CRITICAL_DAMAGE_VALUE] = damage
                        pygame.event.post(self._enemyTakenCriticalDamageEvent)
                    break

            self._currentEnemy.takeDamage(damage)
            self._checkDefeat()

    def finishAttack(self):
        if self._currentEnemy is not None and self._startedAttack:
            self._startedAttack = False
            self._enemyAttackedEvent.dict[EnemyConfig.DAMAGE_VALUE] = -self._currentEnemy.damage
            pygame.event.post(self._enemyAttackedEvent)

    def draw(self):
        if self._currentEnemy is not None:
            self._currentEnemy.draw()