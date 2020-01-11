import pygame
import os
from enemies.skeleton import Skeleton
from enemies.warrior import Warrior
from towers.longRangeTower import LongRangeTower
from towers.enemyBase import EnemyBase
from towers.supportTower import RangeTower, DamageTower
import time
import random

lives_img = pygame.image.load(os.path.join("game_assets/support_stuff", "heart-icon.png"))


class Game:
    def __init__(self):
        self.width = 1600
        self.height = 1000
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = [Warrior()]
        self.units = []
        self.attack_towers = [LongRangeTower(500, 500)]
        self.support_towers = [RangeTower(550, 500), DamageTower(450, 500)]
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("game_assets/support_stuff", "bg3.png"))
        self.timer = time.time()
        self.clicks = []  # TODO: wyrzucić na sam koniec(zostawione by ustawić path na nowej mapie)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            if time.time() - self.timer > random.randrange(1, 5):
                self.timer = time.time()
                self.enemys.append(random.choice([Warrior(), Skeleton()]))
            clock.tick(60)
            # pygame.time.wait(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(pos)
                    print(pos)

            # loop through enemies
            to_del = []
            for en in self.enemys:
                if en.x > 1000:
                    to_del.append(en)
            # delete all the enemies
            for d in to_del:
                self.enemys.remove(d)

            # loop through attack towers
            for t in self.attack_towers:
                if isinstance(t, EnemyBase):
                    t.attack(self.units)
                else:
                    t.attack(self.enemys)

            #loop through support towers
            for t in self.support_towers:
                t.support(self.attack_towers)

            # when you lose
            if self.lives <= 0:
                print("You lose")
                run = False

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))

        # draw clicks
        for p in self.clicks:
            pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)

        # draw enemies
        for en in self.enemys:
            en.draw(self.win)

        # draw attack towers
        for at in self.attack_towers:
            at.draw(self.win)

        #draw support towers
        for st in self.support_towers:
            st.draw(self.win)

        # draw lives
        # TODO: dokonczyc pokazywanie i tracenie zyc(Pjotero)
        life = pygame.transform.scale(lives_img, (32, 32))
        start_x = self.width - life.get_width() - 5
        for x in range(self.lives):
            self.win.blit(life, (start_x - life.get_width() * x + 5, 10))

        pygame.display.update()


g = Game()
g.run()
