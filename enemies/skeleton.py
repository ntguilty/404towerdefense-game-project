import pygame
import os
from enemies.enemy import Enemy

imgs = []
imgs_temp1 = []
imgs_temp2 = []

for x in range(1, 4):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/skeleton", "birds" + add_str + ".png")), (70, 70)))
    imgs_temp1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/skeleton", "birds" + add_str + ".png")), (70, 70)))
for x in range(4, 7):
    add_str = str(x)
    imgs_temp2.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/skeleton", "birds" + add_str + ".png")), (70, 70)))


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "skeleton"
        self.worth = 5
        self.max_health = 2
        self.health = self.max_health
        self.imgs = imgs[:]
        self.imgs_temp2 = imgs_temp2[:]
        self.imgs_temp1 = imgs_temp1[:]
