import os
import pygame
import math


class Enemy:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.animation_count = 0
        self.health = 1
        self.path = [(113, 559), (110, 607),(108, 652), (109, 701), (107, 752), (109, 802), (118, 852), (141, 889), (178, 919),
                     (225, 943), (293, 946), (367, 946), (430, 947), (486, 945), (560, 947), (625, 940), (654, 908), (667, 852),
                     (623, 799), (565, 760), (505, 718), (460, 665), (479, 586), (550, 538), (598, 477), (593, 397), (579, 301),
                     (609, 221), (720, 190), (804, 184), (883, 185), (940, 229), (969, 292), (1006, 362), (951, 424), (930, 480),
                     (887, 539), (915, 593), (968, 667), (1026, 721), (1101, 754), (1185, 765), (1274, 755), (1372, 730),
                     (1436, 661), (1446, 560), (1465, 482), (1460, 409), (1442, 343), (1426, 284), (1410, 232), (1416, 193)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = pygame.image.load(os.path.join("game_assets/enemies/warrior", "warrior1.png"))
        self.path_pos = 0
        self.move_count = 0
        self.move_distance = 0
        self.imgs = []
        self.flipped_vert = False
        self.flipped_hor = False
        self.flipped = False
        self.nextGoal = False
        self.max_health = 0
        self.speed_increase = 5
        self.if_hitted = None

    def draw(self, win):
        """draws the enemy with the given images"""
        self.img = self.imgs[self.animation_count]

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

        if abs(dirn[0]) < abs(dirn[1]):
            self.imgs = self.imgs_temp1
            if dirn[1] > 0 and self.flipped_vert:
                self.flipped_vert = False
                for y, img in enumerate(self.imgs):
                    self.imgs[y] = pygame.transform.flip(img, False, True)
            if dirn[1] < 0 and not self.flipped_vert:
                self.flipped_vert = True
                for y, img in enumerate(self.imgs):
                    self.imgs[y] = pygame.transform.flip(img, False, True)
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


    def hit(self, damage):
        # TODO: dodac animacje uderzenia
        # TODO: dodac dzwiek oznaczajacy ze trafilismy wroga
        """Reduces health by one point and checks if enemy has died each call"""
        self.health -= damage
        if self.health <= 0:
            return True
        return False
