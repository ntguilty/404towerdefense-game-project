import pygame


class Base:
    """Abstract class for base?"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        self.menu = None
        self.imgs = []
        self.damage = 1

    def draw(self, win):
        img = self.imgs[self.level - 1]
        win.blit(img, (self.x - img.get_width()/2, self.y - img.get_height()/2))

    def click(self, X, Y):
        """Returns if tower has been clicked on
        and selects tower if it was clicked"""
        if X < self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def upgrade(self):
        """Upgrades base to higher tier at given cost"""
        self.level += 1
        self.damage += 1

    def get_upgrade_cost(self):
        return self.price[self.level-1]

    def move(self, x, y):
        self.x = x
        self.y = y
