import pygame
import os
from enemies.enemy import Enemy


# do naprawy
class Warior(Enemy):

    def __init__(self):
        super().__init__()
        self.imgs = []
        for x in range(1, 4):
            add_str = str(x)
            self.imgs.append(pygame.transform.scale(
                pygame.image.load(os.path.join("game_assets/enemies/dragon", "dragon" + add_str + ".png")), (48, 48)))
