import pygame

class Menu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.item_names = []
        self.imgs = []
        self.items = 0

    def click(self, x, y):
        pass