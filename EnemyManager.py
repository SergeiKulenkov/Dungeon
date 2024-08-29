from Enemy import Enemy

class EnemyManager:
    def __init__(self):
        self.currentEnemy = None
        self.hardEnemyCooldown = 0

    def spawnEnemy(self):
        self.currentEnemy = Enemy()