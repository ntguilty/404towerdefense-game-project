import pygame
import os
import math
import time
from .tower import Tower
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu.png")), (120,70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upg.png")), (50,50))

# TODO: dodać animacje wież(jakąkolwiek)
class LongRangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imgs = []
        self.oryginal_range = 150
        self.range = self.oryginal_range
        self.inRange = False
        self.left = True
        self.timer = time.time()
        self.oryginal_damage = 1
        self.damage = self.oryginal_damage
        self.width = self.height = 128
        self.price = [2000, 4000, 0]
        temp = []
        for x in range(len(self.price) - 1):
            temp.append(str(self.price[x]))
        temp.append("MAX")
        self.menu = Menu(self, self.x, self.y, menu_bg, temp)
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "longRangeTower"
        self.moving = False



        self.imgs.append(
            pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers/", "base1.png")), (50, 100)))

    def get_upgrade_cost(self):
        return self.price[self.level - 1]

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)
        base = self.imgs[0]

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

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        # to bedzie przydatne w lucznikach.
        # flipowanie obrazka w zaleznosci czy przeciwnik jest z lewej lub prawej strony
        # """
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if time.time() - self.timer > 0.5:
                self.timer = time.time()
                if first_enemy.hit(self.damage) == True:
                    income = first_enemy.worth
                    enemies.remove(first_enemy)
                    return income

            if first_enemy.x > self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)
        return 0
        # """
