import pygame
import os
import math
import time
from .tower import Tower


# TODO: dodać animacje wież(jakąkolwiek)
# TODO: dodac jakiegos normalnego sprita do LongRangeTower
class LongRangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imgs = []
        self.oryginal_range = 200
        self.range = self.oryginal_range
        self.inRange = False
        self.left = True
        self.timer = time.time()
        self.oryginal_damage = 1
        self.damage = self.oryginal_damage
        self.width = self.height = 128

        self.imgs.append(
            pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers/", "base1.png")), (128, 128)))

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

        base = self.imgs[0]
        win.blit(base, ((self.x + self.width / 2) - (base.get_width() / 2), (self.y - base.get_height())))

    def change_range(self, r):
        self.range = r

    def attack(self, enemies):
        """"""
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            en_x = enemy.x
            en_y = enemy.y
            dis = math.sqrt((self.x - en_x) ** 2 + (self.y - en_y) ** 2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.x)
        # to bedzie przydatne w lucznikach.
        # flipowanie obrazka w zaleznosci czy przeciwnik jest z lewej lub prawej strony
        # """
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if time.time() - self.timer > 0.5:
                self.timer = time.time()
                if first_enemy.hit(self.damage) == True:
                    enemies.remove(first_enemy)
            if first_enemy.x > self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)
        # """