import pygame
import os
import math
import time
from .tower import Tower

range_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "range_tower.png")), (128, 128))]


class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 200
        self.effect = [0.2, 0.4]
        self.imgs = range_imgs[:]

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
    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "damage_tower.png")), (128, 128))]


class DamageTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 200
        self.effect = [2, 4]
        self.imgs = damage_imgs[:]

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
