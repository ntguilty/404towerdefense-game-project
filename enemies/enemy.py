import os
import pygame
import math


class Enemy:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.animation_count = 0
        self.health = 1
        self.vel = 2  # velocity - how fast unit moves
        self.path = [(25, 68), (108, 68), (214, 69), (395, 64), (492, 69), (534, 70), (549, 82), (550, 103),
                     (551, 128), (551, 172), (552, 244), (552, 310), (552, 374), (552, 441), (552, 465), (558, 479),
                     (564, 484), (574, 487), (590, 489), (633, 485), (699, 488), (779, 489), (813, 491), (889, 487),
                     (943, 485), (961, 487), (973, 486), (983, 476), (988, 355), (996, 235)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = pygame.image.load(os.path.join("game_assets/enemies/warrior", "warrior1.png"))
        self.path_pos = 0
        self.move_count = 0
        self.move_distance = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0
        self.speed_increase = 1

    def draw(self, win):
        """draws the enemy with the given images"""
        self.img = self.imgs[self.animation_count]

        for dot in self.path:
            pygame.draw.circle(win, (255, 0, 0), dot, 10, 0)
        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 2))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """Draws health bar above unit"""
        lenght = 50
        move_by = lenght / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(win, (255, 0, 0), (self.x - 35, self.y - 40, lenght, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 35, self.y - 40, health_bar, 10), 0)

    def collide(self, X, Y):
        """Returns if the position has hit enemy"""
        if X < self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

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
        dirn = (dirn[0] / length * self.speed_increase, (dirn[1]) / length * self.speed_increase)
        if x1 == 942:
            print(dirn)

        if dirn[0] < 0 and not self.flipped:
            self.flipped = True
            for y, img in enumerate(self.imgs):
                self.imgs[y] = pygame.transform.flip(img, True, False)
        if dirn[0] > 0 and self.flipped:
            self.flipped = False
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
            else:  # moving up
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:  # moving up
                if self.x <= x2 and self.y <= y2:
                    self.path_pos += 1


    def hit(self, damage):
        """Reduces health by one point and checks if enemy has died each call"""
        self.health -= damage
        if self.health <= 0:
            return True
        return False
