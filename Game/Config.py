class GeneralConfig:
    FONT = 'comicsans'
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)
    ORANGE = (207, 142, 109)
    GREEN = (120, 240, 120)
    DOOR_WIDTH = 330
    DOOR_HEIGHT = 380
    ASSETS_PATH = 'Assets'
    IMAGES_PATH = ASSETS_PATH + '\\Images'

class GameConfig:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    MOUSE_POSITION_VALUE = 'mousePosition'

    BORDER_ACTION_OFFSET_X_PERCENT = 0.6
    BORDER_STATS_OFFSET_Y = 100
    BORDER_WIDTH = 5
    DOOR_IMAGE = 'door.png'

    GAME_START_DELAY = 0.75
    FINISH_DELAY = 2

    MAX_NUMBER_OF_ROOMS = 5
    FINISH_TEXT = 'YOU WIN!'
    GAME_OVER_TEXT = 'Game over'
    FINISH_TEXT_SIZE = 65
    FINISH_TEXT_OFFSET_Y = 0.25
    SCORE_TEXT = 'score'
    SCORE_TEXT_SIZE = 35
    SCORE_TEXT_OFFSET = 10

class ButtonsConfig:
    BUTTON_TYPE_VALUE = 'buttonType'

    MENU_BUTTON_WIDTH = 170
    MENU_BUTTON_HEIGHT = 55
    MENU_BUTTON_TEXT_SIZE = 45

    NUMBER_OF_BUTTONS_IN_ROW = 2
    BUTTON_OUTLINE_THICKNESS = 3
    BUTTON_WIDTH = 130
    BUTTON_HEIGHT = 30
    BUTTON_TEXT_SIZE = 25
    BUTTON_OFFSET_FROM_DOOR_Y = 15
    BUTTON_OFFSET_Y = 25

    START_BUTTON_TEXT = 'Start'
    LEAVE_BUTTON_TEXT = 'Leave'
    EAT_BUTTON_TEXT = 'Eat'
    ATTACK_BUTTON_TEXT = 'Attack'
    PARRY_BUTTON_TEXT = 'Parry'
    TAKE_ITEM_BUTTON_TEXT = 'Take Item'
    USE_ITEM_BUTTON_TEXT = 'Use Item'
    QUIT_BUTTON_TEXT = 'Quit'

class RoomConfig:
    ROOMS_CONTENTS_PROBABILITIES = { 'FOOD' : 0.12, 'COMBAT' : 0.65, 'ITEM' : 0.23 }
    ROOM_TYPE_VALUE = 'roomType'
    FOOD_HP_VALUE = 'foodHP'
    ITEM_VALUE = 'item'
    ARTIFACT_PROBABILITY = 0.25
    MAX_ITEMS_IN_ROW = 2
    MAX_FOOD_IN_ROW = 1
    NEXT_ROOM_DELAY = 0.5

class ActionLogConfig:
    ACTION_LOG_OFFSET_X = 25
    ACTION_LOG_OFFSET_Y = 15
    ACTION_LOG_TEXT_SIZE = 12
    ACTION_LOG_GAP = 6

    GREETING_MESSAGE = 'Welcome to the dungeon!'
    ROOM_ENTERED_MESSAGE = 'Room entered.'
    FOOD_ROOM_MESSAGE = 'You find some precious food.'
    ITEM_ROOM_MESSAGE = 'You find a useful item.'
    FULL_HEALTH_MESSAGE = 'You are already at full health.'
    HEAL_MESSAGE = 'You heal {0} health.'
    ITEM_TAKEN_MESSAGE = 'You take the {0}.'
    ITEM_USED_MESSAGE = 'You use the {0}.'
    HURT_MESSAGE = 'You take {0} damage.'
    DIED_MESSAGE = 'You died...'
    ATTACK_MESSAGE = 'You deal {0} damage to the enemy.'
    TRY_PARRY_MESSAGE = 'You try to parry the next attack.'
    PARRY_SUCCESS_MESSAGE = 'You successfully parried the attack.'
    PARRY_FAIL_MESSAGE = 'Your parry failed.'
    ENEMY_SPAWNED_MESSAGE = 'You find a {0} {1}.'
    ENEMY_DEFEATED_MESSAGE = 'You defeated the {0}!'
    ENEMY_CRITICAL_DAMAGE = 'You deal {0} critical damage!'

    ENEMY_ADJECTIVES = ['frightful', 'horrible', 'terrible', 'dreadful']

class StatsConfig:
    STATS_OFFSET_FROM_BORDER_X = 25
    STATS_OFFSET_FROM_BORDER_Y = 35
    STAT_VALUE_OFFSET = 10
    STATS_GAP = 25
    STAT_TEXT_SIZE = 20

    HEALTH_STAT_NAME = 'Health'
    DAMAGE_STAT_NAME = 'Damage'
    ARMOUR_STAT_NAME = 'Armour'
    LUCK_STAT_NAME = 'Luck'
    STATS_COLOURS = { HEALTH_STAT_NAME : (25, 130, 30),
                      DAMAGE_STAT_NAME : (180, 0 ,0),
                      ARMOUR_STAT_NAME : (50, 50, 180),
                      LUCK_STAT_NAME : (190, 190, 40) }

class FoodConfig:
    FOOD_IMAGE = 'food.png'
    FOOD_WIDTH = 100
    FOOD_HEIGHT = 80
    MIN_HP = 2
    MAX_HP = 5

class ItemsConfig:
    BOW_IMAGE = 'bow.png'
    BOMB_IMAGE = 'bomb.png'
    AXE_IMAGE = 'axe.png'
    SCROLL_IMAGE = 'scroll.png'
    TREASURE_IMAGE = 'treasure.png'

    BOW_NAME = 'BOW'
    BOMB_NAME = 'BOMB'
    SCROLL_NAME = 'MAGIC_SCROLL'

    ITEM_WIDTH = 125
    ITEM_HEIGHT = 125
    ITEM_WIDTH_INVENTORY = 50
    ITEM_HEIGHT_INVENTORY = 50

    BOW_POWER = 5
    BOMB_POWER = 5
    AXE_POWER = 5
    MAGIC_SCROLL_POWER = 25

class EnemyConfig:
    ENEMY_WIDTH = 280
    ENEMY_HEIGHT = 280
    ENEMY_STATS_OFFSET_Y = 50
    EASY_ENEMIES_IN_A_ROW = 2
    EASY_ENEMY_COOLDOWN = 1
    HARD_ENEMY_COOLDOWN = 1
    ENEMY_ATTACK_DELAY = 0.75
    REMOVE_ENEMY_DELAY = 1

    TYPE_VALUE = 'enemyType'
    DAMAGE_VALUE = 'damage'
    CRITICAL_DAMAGE_VALUE = 'critical'

    SKELETON_NAME = 'SKELETON'
    GOBLIN_NAME = 'GOBLIN'
    ORC_NAME = 'ORC'
    SPIDER_NAME = 'SPIDER'

    SKELETON_IMAGE = 'skeleton.png'
    GOBLIN_IMAGE = 'goblin.png'
    ORC_IMAGE = 'orc.png'
    SPIDER_IMAGE = 'spider.png'

    ENEMIES_PROBABILITIES = { SKELETON_NAME : 0.40, GOBLIN_NAME : 0.30, ORC_NAME : 0.15, SPIDER_NAME : 0.15 }
    SKELETON_STATS = { StatsConfig.HEALTH_STAT_NAME : 5, StatsConfig.DAMAGE_STAT_NAME : 1 }
    GOBLIN_STATS = { StatsConfig.HEALTH_STAT_NAME : 10, StatsConfig.DAMAGE_STAT_NAME : 2 }
    ORC_STATS = { StatsConfig.HEALTH_STAT_NAME : 15, StatsConfig.DAMAGE_STAT_NAME : 3 }
    SPIDER_STATS = { StatsConfig.HEALTH_STAT_NAME : 20, StatsConfig.DAMAGE_STAT_NAME : 4 }

    # values are damage multipliers for these scenarios
    ITEM_INTERACTIONS = { (ItemsConfig.BOW_NAME, SPIDER_NAME) : 10,
                          (ItemsConfig.BOW_NAME, ORC_NAME) : 0.5,
                          (ItemsConfig.BOMB_NAME, GOBLIN_NAME) : 2 }

class CharacterConfig:
    ATTACK_VALUE = 'damage'
    HP_CHANGE_VALUE = 'hp'
    ITEM_TYPE_VALUE = 'itemType'
    ITEM_POWER_VALUE = 'itemPower'
    ITEM_OFFSET_FROM_STATS_X = 100
    ITEM_OFFSET_FROM_BORDER = 25

    MAX_PARRY_LUCK = 10
    PARRY_DAMAGE_MULTIPLIER = 2

    BASE_STATS = { StatsConfig.HEALTH_STAT_NAME: 10,
                   StatsConfig.DAMAGE_STAT_NAME: 10,
                   StatsConfig.ARMOUR_STAT_NAME: 2,
                   StatsConfig.LUCK_STAT_NAME: 5 }
    ENEMY_SCORE = { EnemyConfig.SKELETON_NAME : 10,
                    EnemyConfig.GOBLIN_NAME : 15,
                    EnemyConfig.ORC_NAME : 20,
                    EnemyConfig.SPIDER_NAME : 30 }
    ITEM_SCORE = 20
    MAGIC_SCROLL_SCORE = 50
    MIN_TREASURE_SCORE = 25
    MAX_TREASURE_SCORE = 50
    SCORE_ENEMY_TEXT = 'enemies'
    SCORE_TREASURE_TEXT = 'treasure'
    SCORE_ITEM_TEXT = 'items'
