from game import Game
from multi import Multiplayer
import pygame
import os

start_btn_single = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "one_player.png")).convert_alpha(), (250,250))
start_btn_double = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "two_players.png")).convert_alpha(), (250,250))
logo = pygame.image.load(os.path.join("game_assets/support_stuff", "logo.png")).convert_alpha()

class MainMenu:
    def __init__(self):
        self.width = 1600
        self.height = 1000
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_stuff", "map.png")),
                                         (1600, 1000))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.win = pygame.display.set_mode((self.width, self.height))
        self.btn= (self.width/2 - start_btn_single.get_width()/2 - 250, 500, start_btn_single.get_width(), start_btn_single.get_height())
        self.mult_btn = (self.width/2 - start_btn_double.get_width()/2 + 250, 500, start_btn_double.get_width(), start_btn_double.get_height())

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    if self.btn[0] <= x <= self.btn[0] + self.btn[2]:
                        if self.btn[1] <= y <= self.btn[1] + self.btn[3]:
                            game = Game()
                            game.run()
                            del game
                    if self.mult_btn[0] <= x <= self.mult_btn[0] + self.mult_btn[2]:
                        if self.mult_btn[1] <= y <= self.mult_btn[1] + self.mult_btn[3]:
                            game = Multiplayer()
                            game.run()
                            del game
            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0,0))
        self.win.blit(logo, (self.width/2 - logo.get_width()/2, 0))
        self.win.blit(start_btn_single, (self.btn[0], self.btn[1]))
        self.win.blit(start_btn_double, (self.width/2 - start_btn_single.get_width()/2 + 250, 500))
        pygame.display.update()