import pygame


class Tower:
    """Abstract class for towers?"""
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

    def draw_radius(self, win):
        if self.selected:
            # draw range circle
            circle_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(circle_surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(circle_surface, (self.x - self.range, self.y - self.range))

    def click(self, X, Y):
        """Returns if tower has been clicked on
        and selects tower if it was clicked"""
        img = self.imgs[self.level - 1]
        if X <= self.x - img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
            if Y <= self.y + self.height - img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False

    def upgrade(self):
        """Upgrades towers to higher tier at given cost"""
        self.level += 1
        self.damage += 1

    def get_upgrade_cost(self):
        return self.price[self.level-1]

    def move(self, x, y):
        self.x = x
        self.y = y
