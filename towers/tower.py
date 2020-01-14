import pygame
import os
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu.png")), (120, 70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "one_player.png")), (50, 50))


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.range = 0
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        # define menu and buttons
        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.imgs = []
        self.damage = 1

    def draw(self, win):
        # TODO: dodaj wiecej spritow zeby pokazac ulepszanie wiez, ustawione normalnie na self.level - 1
        img = self.imgs[0]
        win.blit(img, (self.x - img.get_width() / 2, self.y - img.get_height() / 2))

        # draw menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self, win):
        if self.selected:
            # draw range circle
            circle_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(circle_surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(circle_surface, (self.x - self.range, self.y - self.range))

    def click(self, X, Y):
        """Returns if tower has been clicked on
        and selects tower if it was clicked"""
        # tu zmienione również z self.level - 1 na 0 z powodu brakow spritow
        img = self.imgs[0]
        if X <= self.x - img.get_width() // 2 + self.width and X >= self.x - img.get_width() // 2:
            if Y <= self.y + self.height - img.get_height() // 2 and Y >= self.y - img.get_height() // 2:
                return True
        return False

    def upgrade(self):
        """Upgrades towers to higher tier at given cost"""
        # instead of next sprites is only block by number
        if self.level < 2:
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        return self.price[self.level - 1]

    def move(self, x, y):
        self.x = x
        self.y = y
