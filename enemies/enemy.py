import pygame
import math


class Enemy:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.animation_count = 0
        self.health = 1
        self.vel = 2 # velocity - how fast unit moves
        self.path = [(-10,65), (7, 65), (266, 67), (250, 70), (558, 74), (530, 65), (558, 259), (558, 489), (773, 486), (942, 485), (947, 247), (1050, 250)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.path_pos = 0
        self.move_count = 0
        self.move_distance = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0

    def draw(self, win):
        """draws the enemy with the given images"""
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        self.img = self.imgs[self.animation_count]

        for dot in self.path:
            pygame.draw.circle(win, (255,0,0), dot,10, 0)
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_var(win)
        self.move()

    def draw_health_var(self, win):
        """Draws health bar above unit"""
        lenght = 50
        move_by = round(lenght / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255, 0, 0), (self.x - 25, self.y - 30, lenght, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 25, self.y - 30, health_bar, 10), 0)

    def collide(self, X, Y):
        """Returns if the position has hit enemy"""
        if X < self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        """Moves enemy"""
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (1100, 250)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        move_dis = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

       # self.move_count += 1
        dirn = ((x2 - x1), (y2 - y1))
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = ((dirn[0])/length, (dirn[1])/length)

        if dirn[0] < 0 and not (self.flipped):
            self.flipped = True
            for y, img in enumerate(self.imgs):
                self.imgs[y] = pygame.transform.flip(img, True, False)

        move_x, move_y = (self.x + dirn[0], self.y + dirn[1])
        self.x = move_x
        self.y = move_y
        # go to the next point
        if dirn[0] >= 0: #moving right
            if dirn[1] >= 0: #moving down
                if self.x >= x2 and self.y >= y2:
                    self.move_distance = 0
                    self.path_pos += 1
            else:#moving up
                if self.x >= x2 and self.y <= y2:
                    self.move_distance = 0
                    self.path_pos += 1
        else:#moving left
            if dirn[1] >= 0: #moving down
                if self.x <= x2 and self.y >= y2:
                    self.move_distance = 0
                    self.path_pos += 1
            else:#moving up
                if self.x <= x2 and self.y >= y2:
                    self.move_distance = 0
                    self.path_pos += 1


    def hit(self):
        """Reduces health by one point and checks if enemy has died each call"""
        self.health -= 1
        if self.health <= 0:
            return True
        return False
