import pygame
import os
import math
import time
from .allyBase import AllyBase


# TODO: jak sie uda to bedzie to baza 2giego gracza
# TODO: jak na razie nie jest wykorzystana ta klasa
class EnemyBase(AllyBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imgs = []
        self.range = 200
        self.inRange = False
        self.left = True
        self.timer = time.time()
        self.damage = 1

        self.imgs.append(
            pygame.transform.scale(pygame.image.load(os.path.join("game_assets/bases/", "base1.png")), (128, 128)))
