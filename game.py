import pygame
import os
from enemies.skeleton import Skeleton
from enemies.warrior import Warrior
from menu.menu import PlayPauseButton
from towers.longRangeTower import LongRangeTower
from towers.enemyBase import EnemyBase
from towers.supportTower import RangeTower, DamageTower
from menu.menu import VerticalMenu
import time
import random

pygame.init()
pygame.display.set_mode((1600, 1000))



lives_img = pygame.image.load(os.path.join("game_assets/support_stuff", "heart-icon.png"))
money_img = pygame.image.load(os.path.join("game_assets/support_stuff", "money.png"))

vertical_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "vertical_menu.png")), (100, 450))

longRangeshortcut = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "base1.png")), (50, 70))
rangeShortcut = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "damage_tower.png")), (70, 70))
damageShortcut = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "range_tower.png")), (70, 70))


play_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_stuff", "play_button.png")),
                                  (75, 75))
pause_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_stuff", "pause_button.png")),
                                   (75, 75))
play_btn = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets/support_stuff", "play_button.png")).convert_alpha(), (75, 75))
pause_btn = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets/support_stuff", "pause_button.png")).convert_alpha(), (75, 75))

attack_tower_names = ['LongRangeTower']
support_tower_names = ['RangeTower', 'DamageTower']

# TODO: jak juz doda sie wiecej przeciwnikow to trzeba je zupdatowac. Moze nawet wymyslec lepszy sposob na ich
#  wysylanie (Kacpur) fale przeciwnikow format : (# skeleton, # warrior)

waves = [
    [15, 0],
    [30, 0],
    [50, 0],
    [0, 15],
    [0, 30],
    [0, 50],
    [10, 10],
    [20, 20],
    [30, 30]
]


class Game:
    def __init__(self):
        self.width = 1600
        self.height = 1000
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.units = []
        self.attack_towers = [LongRangeTower(840, 420)]
        self.support_towers = [RangeTower(810, 500), DamageTower(660, 300)]
        self.lives = 10
        self.money = 500000
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_stuff", "map.png")), (1600, 1000))
        self.timer = time.time()
        self.font = pygame.font.SysFont("comicsans", 35)
        self.clicks = []  # TODO: wyrzucić na sam koniec(zostawione by ustawić path na nowej mapie)
        self.selected_tower = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = True
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)
        self.menu = VerticalMenu(self.width - vertical_img.get_width() - 5, 200, vertical_img)
        self.menu.add_btn(longRangeshortcut, "longRangeTower", 500)
        self.menu.add_btn(rangeShortcut, "rangeTower", 750)
        self.menu.add_btn(damageShortcut, "damageTower", 1000)
        self.moving_object = None

    def gen_enemies(self):
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
                self.playPauseButton.paused = self.pause
        else:
            wave_enemies = [Skeleton(), Warrior()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            # generowanie potworow:
            # TODO: ten if jest do usuniecia jak sie wstawi przycisk do wypuszczenia fali
#            if len(self.enemys) == 0:
#                self.pause = False
            if self.pause == False:
                if time.time() - self.timer > random.randrange(1, 5):
                    self.timer = time.time()
                    self.gen_enemies()

            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.attack_towers[:] + self.support_towers[:]
                collide = False
                for tower in tower_list:
                    if tower.collide(self.moving_object):
                        collide = True
                        tower.place_color = (255, 0, 0, 100)
                        self.moving_object.place_color = (255, 0, 0, 100)
                    else:
                        tower.place_color = (0, 0, 255, 100)
                        if not collide:
                            self.moving_object.place_color = (0, 0, 255, 100)


            # main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # odkomentowac i zakomentowac inne przy ustalaniu nowego path na mapie
                    # self.clicks.append(pos)
                    # print(pos)
                    # sprawdzanie przyciskow pauza/graj:
                    if self.playPauseButton.click(pos[0], pos[1]):
                        self.pause = not (self.pause)
                        self.playPauseButton.paused = self.pause

                    # look if you clicked on attack tower or support tower
                    btn_clicked = None
                    if self.selected_tower:
                        btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                        if btn_clicked:
                            if btn_clicked == "Upgrade":
                                cost = self.selected_tower.get_upgrade_cost()
                                if self.money >= cost:
                                    if self.selected_tower.upgrade() == True:
                                        self.money -= cost

                    if not (btn_clicked):
                        for t in self.attack_towers:
                            if t.click(pos[0], pos[1]):
                                t.selected = True
                                self.selected_tower = t
                            else:
                                t.selected = False

                        # look if you clicked on support tower
                        for t in self.support_towers:
                            if t.click(pos[0], pos[1]):
                                t.selected = True
                                self.selected_tower = t
                            else:
                                t.selected = False

            if not (self.pause):
                # loop through enemies
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.x > 1000:
                        to_del.append(en)
                # delete all the enemies
                for d in to_del:
                    self.enemys.remove(d)

                # TODO: jesli sie uda zrobic przeciwnika to trzeba zupdatowac atak o dodawanie pieniedzy
                # loop through attack towers
                for t in self.attack_towers:
                    if isinstance(t, EnemyBase):
                        t.attack(self.units)
                    else:
                        self.money += t.attack(self.enemys)

                # loop through support towers
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

        # draw support towers
        for st in self.support_towers:
            st.draw(self.win)

        # draw vertical menu
        self.menu.draw(self.win)


        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)


        # draw play pause button
        self.playPauseButton.draw(self.win)

        # TODO: trzeba trzeba ladnie ulozyc zycia i pieniadze
        # draw money
        text = self.font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(money_img, (35, 35))
        start_x = self.width - 35

        self.win.blit(text, (start_x - text.get_width() - 1, 42))
        self.win.blit(money, (start_x, 35))

        # draw lives
        # TODO: dokonczyc pokazywanie i tracenie zyc(Pjotero)
        life = pygame.transform.scale(lives_img, (32, 32))
        start_x = self.width - life.get_width() - 5
        for x in range(self.lives):
            self.win.blit(life, (start_x - life.get_width() * x + 5, 10))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["longRangeTower", "damageTower", "rangeTower"]
        object_list = [LongRangeTower(x, y), DamageTower(x, y), RangeTower(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")




g = Game()
g.run()
