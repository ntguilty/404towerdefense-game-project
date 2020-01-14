import pygame
import os
from enemies.enemy import Enemy

imgs = []

for x in range(1, 4):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/skeleton", "birds" + add_str + ".png")), (70, 70)))


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "skeleton"
        self.worth = 5
        self.max_health = 2
        self.health = self.max_health
        self.imgs = imgs[:]
