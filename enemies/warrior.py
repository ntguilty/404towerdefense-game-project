import pygame
import os
from enemies.enemy import Enemy

imgs = []

for x in range(1, 4):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/warrior", "warrior" + add_str + ".png")), (48, 48)))


class Warrior(Enemy):

    def __init__(self):
        super().__init__()
        self.imgs = imgs[:]
        self.max_health = 4
        self.health = self.max_health