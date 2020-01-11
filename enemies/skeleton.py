import pygame
import os
from enemies.enemy import Enemy


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.imgs = []

        for x in range(1, 6):
            add_str = str(x)
            add_str = "0" + add_str
            self.imgs.append(pygame.transform.scale(
                pygame.image.load(os.path.join("game_assets/enemies/skeleton", "skeleton" + add_str + ".png")), (48, 48)))

