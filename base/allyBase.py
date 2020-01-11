import pygame
import os
import math
import time
from .base import Base

# TODO: dodać animacje wież(jakąkolwiek)
class AllyBase(Base):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imgs = []
        self.range = 200
        self.inRange = False
        self.left = True
        self.timer = time.time()
        self.damage = 1

        self.imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/bases/", "base1.png")), (128, 128)))

    def draw(self, win):
        #draw range circle
        circle_surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA, 32)
        pygame.draw.circle(circle_surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

        win.blit(circle_surface, (self.x - self.range, self.y - self.range))
        super().draw(win)

        base = self.imgs[0]
        win.blit(base, ((self.x + self.width/2) - (base.get_width()/2), (self.y - base.get_height())))

    def change_range(self, r):
        self.range = r

    def attack(self, enemies):
        """"""
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            en_x = enemy.x
            en_y = enemy.y
            dis = math.sqrt((self.x - en_x)**2 + (self.y - en_y)**2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda  x: x.x)
        # to bedzie przydatne w lucznikach.
        #flipowanie obrazka w zaleznosci czy przeciwnik jest z lewej lub prawej strony
        #"""
        if len(enemy_closest)>0:
            first_enemy = enemy_closest[0]
            if time.time() - self.timer > 0.5:
                self.timer = time.time()
                if first_enemy.hit() == True:
                    enemies.remove(first_enemy)
            if first_enemy.x > self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.imgs):
                    self.imgs[x] = pygame.transform.flip(img, True, False)
        #"""
