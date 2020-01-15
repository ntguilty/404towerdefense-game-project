import pygame
import os
import math
import time

from menu.menu import Menu
from .tower import Tower

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu.png")), (120, 70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upg.png")), (50, 50))
range_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "range_tower.png")), (100, 100))]


class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 150
        self.effect = [0.2, 0.4]
        self.imgs = range_imgs[:]
        self.width = self.height = 128
        self.price = [14000, 0]
        temp = []
        for x in range(len(self.price) - 1):
            temp.append(str(self.price[x]))
        temp.append("MAX")
        self.menu = Menu(self, self.x, self.y, menu_bg, temp)
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "rangeTower"


    def get_upgrade_cost(self):
        return self.price[self.level - 1]

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def support(self, towers):
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y
            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis <= self.range + tower.width/2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.oryginal_range + round(tower.range * self.effect[self.level - 1])


damage_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "damage_tower.png")), (100, 100))]


class DamageTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 150
        self.effect = [2, 4]
        self.imgs = damage_imgs[:]
        self.width = self.height = 128
        self.price = [1300, 0]
        temp = []
        for x in range(len(self.price) - 1):
            temp.append(str(self.price[x]))
        temp.append("MAX")
        self.menu = Menu(self, self.x, self.y, menu_bg, temp)
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "damageTower"

    def get_upgrade_cost(self):
        return self.price[self.level - 1]


    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def support(self, towers):
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y
            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis <= self.range + tower.width/2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.oryginal_damage * self.effect[self.level - 1]


