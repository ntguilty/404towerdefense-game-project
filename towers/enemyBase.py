import pygame
import os
import math
import time
from .longRangeTower import LongRangeTower


# TODO: jak sie uda to bedzie to baza 2giego gracza,a jak na razie nie jest wykorzystana ta klasa
class EnemyBase(LongRangeTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imgs = []
        self.oryginal_range = 200
        self.range = self.oryginal_range
        self.inRange = False
        self.left = True
        self.timer = time.time()
        self.damage = 1

        self.imgs.append(
            pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers/", "base1.png")), (128, 128)))
