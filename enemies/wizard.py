import math
import pygame
import os
from enemies.enemy import Enemy

imgs = []
imgs_temp1 = []
imgs_temp2 = []
imgs_temp3 = []

for x in range(1, 4):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/wizard", "wizard" + add_str + ".png")), (48, 48)))
    imgs_temp1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/wizard", "wizard" + add_str + ".png")), (48, 48)))
for x in range(4, 7):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/wizard", "wizard" + add_str + ".png")), (48, 48)))
    imgs_temp2.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/wizard", "wizard" + add_str + ".png")), (48, 48)))
for x in range(7, 10):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/wizard", "wizard" + add_str + ".png")), (48, 48)))
    imgs_temp3.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/enemies/wizard", "wizard" + add_str + ".png")), (48, 48)))


class Wizard(Enemy):

    def __init__(self):
        super().__init__()
        self.name = "wizard"
        self.worth = 25
        self.imgs = imgs[:]
        self.imgs_temp2 = imgs_temp2[:]
        self.imgs_temp1 = imgs_temp1[:]
        self.imgs_temp3 = imgs_temp3[:]
        self.max_health = 10
        self.health = self.max_health

    # this method needs to be overwriten in warior becouse of the sprites.
    def move(self):
        """Moves enemy"""
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (1100, 250)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        # self.move_count += 1
        dirn = ((x2 - self.x)*2, (y2 - self.y)*2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length * self.speed_increase, dirn[1] / length * self.speed_increase)
        if abs(dirn[0]) < abs(dirn[1]):
            if dirn[1] > 0:
                self.imgs = self.imgs_temp1
            else:
                self.imgs = self.imgs_temp3
        else:
            self.imgs = self.imgs_temp2
            if dirn[0] > 0 and self.flipped_hor:
                self.flipped_hor = False
                for y, img in enumerate(self.imgs):
                    self.imgs[y] = pygame.transform.flip(img, True, False)
            if dirn[0] < 0 and not self.flipped_hor:
                self.flipped_hor = True
                for y, img in enumerate(self.imgs):
                    self.imgs[y] = pygame.transform.flip(img, True, False)

        move_x, move_y = (self.x + dirn[0], self.y + dirn[1])
        self.x = move_x
        self.y = move_y
        # go to the next point
        if dirn[0] >= 0:  # moving right
            if dirn[1] >= 0:  # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
                    self.nextGoal = True
            else:  # moving up
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
                    self.nextGoal = True
        else:  # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
                    self.nextGoal = True
            else:  # moving up
                if self.x <= x2 and self.y <= y2:
                    self.path_pos += 1
                    self.nextGoal = True