import pygame
import os
from enemies.skeleton import Skeleton
from enemies.warior import Warior
from base.allyBase import AllyBase
import time
import random


class Game:
    def __init__(self):
        self.width = 1000
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = [Warior()]
        self.units = []
        self.towers = [AllyBase(500, 500)]
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("game_assets/support_stuff", "bg3.png"))
        self.timer = time.time()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            if time.time() - self.timer > random.randrange(1,5):
                self.timer = time.time()
                self.enemys.append(random.choice([Warior(), Skeleton()]))
            clock.tick(60)
            #pygame.time.wait(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            # loop through enemies
            to_del = []
            for en in self.enemys:
                if en.x > 1000:
                    to_del.append(en)
            #delete all the enemies
            for d in to_del:
                self.enemys.remove(d)

            #loop through bases
            for b in self.towers:
                b.attack(self.enemys)
            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))

        # draw enemies
        for en in self.enemys:
            en.draw(self.win)

        #draw bases
        for b in self.towers:
            b.draw(self.win)

        pygame.display.update()

g = Game()
g.run()