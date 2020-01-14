import pygame
import os
from enemies.enemy import Enemy

imgs = []

for x in range(1, 5):
    add_str = str(x)
    add_str = "0" + add_str
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/skeleton", "skeleton" + add_str + ".png")), (48, 48)))


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "skeleton"
        self.worth = 5
        self.max_health = 2
        self.health = self.max_health
        self.imgs = imgs[:]
