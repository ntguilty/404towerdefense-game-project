import pygame
import time
import os
import random
from enemies.skeleton import Skeleton
from enemies.warrior import Warrior
from enemies.wizard import Wizard
from enemies.boss import Boss
from menu.menu import PlayPauseButton
from towers.longRangeTower import LongRangeTower
from towers.enemyBase import EnemyBase
from towers.supportTower import RangeTower, DamageTower
from menu.menu import VerticalMenu
from game import Game

pygame.init()
pygame.display.set_mode((1600, 1000))

money_img = pygame.image.load(os.path.join("game_assets/support_stuff", "money.png"))
vertical_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "vertical_menu.png")), (100, 450))

longRangeshortcut = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "base1.png")), (50, 70))
rangeShortcut = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "damage_tower.png")),
                                       (70, 70))
damageShortcut = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/towers", "range_tower.png")),
                                        (70, 70))

play_btn = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets/support_stuff", "play_button.png")).convert_alpha(), (75, 75))
pause_btn = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets/support_stuff", "pause_button.png")).convert_alpha(), (75, 75))

attack_tower_names = ['longRangeTower']
support_tower_names = ['rangeTower', 'damageTower']

# load music and "mute"/"unmute" buttons
pygame.mixer.music.load(os.path.join("game_assets/support_stuff/music", "music1.mp3"))
sound_btn = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets/support_stuff/music", "sound_on_button.png")).convert_alpha(), (75, 75))
sound_btn_off = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets/support_stuff/music", "sound_off_button.png")).convert_alpha(),
    (75, 75))


class Multiplayer:
    def __init__(self):
        # super().__init__()
        self.width = 1600
        self.height = 1000
        self.win = pygame.display.set_mode((self.width, self.height))
        self.player1 = Game()
        self.player1.win = self.win
        self.player2 = Game()
        self.player2.win = self.win
        self.current_player = self.player1
        self.playersTurn = 0
        self.pointsGained = 0
        self.timer = time.time()
        self.font = pygame.font.SysFont("comicsans", 35)
        self.selected_tower = None
        self.switchButton = PlayPauseButton(play_btn, pause_btn, 100, 20)
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 10, self.height - 85)
        self.soundButton = PlayPauseButton(sound_btn, sound_btn_off, 10 + self.playPauseButton.width, self.height - 85)
        self.startRoundButton = PlayPauseButton(pause_btn, play_btn, 100, 100)
        self.current_wave = []
        self.pause = True
        self.switch = False
        self.start = False
        self.music_on = True
        self.startRoundButton.paused = self.start  # this line is made so the image will be drawn correctly
        self.menu = VerticalMenu(self.width - vertical_img.get_width() - 5, 200, vertical_img)
        self.menu.add_btn(longRangeshortcut, "longRangeTower", 500)
        self.menu.add_btn(rangeShortcut, "rangeTower", 750)
        self.menu.add_btn(damageShortcut, "damageTower", 1000)
        self.moving_object = None

    def switch_players(self):
        self.current_player.points += 30 + self.pointsGained
        self.pointsGained = 0
        if self.playersTurn == 0:
            self.current_player = self.player2
            self.playersTurn = 1
        else:
            self.current_player = self.player1
            self.playersTurn = 0
        self.start = False
        self.startRoundButton.paused = False

    def gen_enemies(self):
        if len(self.current_wave) > 0:
            if self.playersTurn == 1:
                self.current_wave[0].path.reverse()
                self.current_wave[0].x = self.current_wave[0].path[0][0]
                self.current_wave[0].y = self.current_wave[0].path[0][1]
            self.current_player.enemys.append(self.current_wave[0])
            self.current_wave.pop(0)
        else:
            self.start = False

    def run(self):
        pygame.mixer.music.play(loops=-1)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            # generowanie potworow:
            if self.start == True and self.pause == True:
                if time.time() - self.timer > random.randrange(1, 5):
                    self.timer = time.time()
                    self.gen_enemies()

            pos = pygame.mouse.get_pos()

            # check for moving object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])
                tower_list = self.current_player.attack_towers[:] + self.current_player.support_towers[:]
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

                # jak sie klika przyciski na klawiaturze to dodaje do fali i odejmuje z punktow gracza
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if self.current_player.points >= 5:
                            self.current_player.points -= 5
                            self.current_wave.append(Skeleton())
                    if event.key == pygame.K_w:
                        if self.current_player.points >= 10:
                            self.current_player.points -= 10
                            self.current_wave.append(Warrior())
                    if event.key == pygame.K_e:
                        if self.current_player.points >= 15:
                            self.current_player.points -= 15
                            self.current_wave.append(Wizard())
                    if event.key == pygame.K_r:
                        if self.current_player.points >= 150:
                            self.current_player.points -= 150
                            self.current_wave.append(Boss())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # przycik pauzy gry
                    if self.playPauseButton.click(pos[0], pos[1]):
                        self.pause = not (self.pause)
                        self.playPauseButton.paused = self.pause

                    # przycisk zamiany graczy
                    if self.switchButton.click(pos[0], pos[1]):
                        if len(self.current_wave) == 0 and len(
                                self.current_player.enemys) == 0 and self.current_player.points == 0:
                            self.switch_players()

                    # przycisk startu fali przeciwnikow
                    if self.startRoundButton.click(pos[0], pos[1]):
                        if self.current_player.points == 0 and len(self.current_player.enemys) == 0:
                            self.start = not (self.start)
                            self.startRoundButton.paused = self.start

                    # if youre moving an object and click
                    if self.moving_object:
                        not_allowed = False
                        tower_list = self.current_player.attack_towers[:] + self.current_player.support_towers[:]
                        for tower in tower_list:
                            if tower.collide(self.moving_object):
                                not_allowed = True
                        if not not_allowed:
                            if self.moving_object.name in attack_tower_names:
                                self.current_player.attack_towers.append(self.moving_object)
                            elif self.moving_object.name in support_tower_names:
                                self.current_player.support_towers.append(self.moving_object)
                            self.moving_object.moving = False
                            self.moving_object = None
                    else:
                        # look if you click on side menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.current_player.money >= cost:
                                self.current_player.money -= cost
                                self.add_tower(side_menu_button)
                            else:
                                print("You don't have enough money")

                        # odkomentowac i zakomentowac inne przy ustalaniu nowego path na mapie
                        # self.clicks.append(pos)
                        # print(pos)
                        # sprawdzanie przyciskow wlaczania muzyki:
                        if self.current_player.soundButton.click(pos[0], pos[1]):
                            self.music_on = not (self.music_on)
                            self.current_player.soundButton.paused = self.music_on
                            if self.music_on:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()

                        # look if you clicked on attack tower or support tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.current_player.money >= cost:
                                        if self.selected_tower.upgrade() == True:
                                            self.current_player.money -= cost

                        if not (btn_clicked):
                            for t in self.current_player.attack_towers:
                                if t.click(pos[0], pos[1]):
                                    t.selected = True
                                    self.selected_tower = t
                                else:
                                    t.selected = False

                            # look if you clicked on support tower
                            for t in self.current_player.support_towers:
                                if t.click(pos[0], pos[1]):
                                    t.selected = True
                                    self.selected_tower = t
                                else:
                                    t.selected = False

            if self.pause:
                # loop through enemies
                to_del = []
                for en in self.current_player.enemys:
                    en.move()
                    if en.nextGoal == True:
                        self.pointsGained += 5
                        en.worth += 1
                        en.nextGoal = False
                    if self.playersTurn == 0:
                        if en.x > 1250 and en.y < 225:
                            to_del.append(en)
                    elif self.playersTurn == 1:
                        if en.x < 115 and en.y > 600:
                            to_del.append(en)
                # delete all the enemies
                for d in to_del:
                    self.current_player.lives -= 1
                    self.current_player.enemys.remove(d)

                # loop through attack towers
                for t in self.current_player.attack_towers:
                    self.current_player.money += t.attack(self.current_player.enemys)

                # loop through support towers
                for t in self.current_player.support_towers:
                    t.support(self.current_player.attack_towers)
                # when you lose
                if self.current_player.lives <= 0:
                    print("You lose")
                    run = False

            self.draw()
        pygame.quit()

    def draw(self):
        self.win.blit(self.current_player.bg, (0, 0))

        if self.moving_object:
            for tower in self.current_player.attack_towers:
                tower.draw_placement(self.win)

            for tower in self.current_player.support_towers:
                tower.draw_placement(self.win)

            self.moving_object.draw_placement(self.win)

        # draw enemies
        for en in self.current_player.enemys:
            en.draw(self.win)

        # draw attack towers
        for at in self.current_player.attack_towers:
            at.draw(self.win)

        # draw support towers
        for st in self.current_player.support_towers:
            st.draw(self.win)

        # draw vertical menu
        self.menu.draw(self.win)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.win)

        # draw sound on/off button
        self.current_player.soundButton.draw(self.win)

        # TODO: trzeba trzeba ladnie ulozyc zycia i pieniadze
        # draw money
        text = self.font.render(str(self.current_player.money), 1, (255, 255, 255))
        money = pygame.transform.scale(money_img, (35, 35))
        start_x = self.width - 35

        self.win.blit(text, (start_x - text.get_width() - 1, 10))
        self.win.blit(money, (start_x, 10))

        # draw lives
        # TODO: dokonczyc pokazywanie i tracenie zyc(Pjotero)
        lenght = 300
        move_by = lenght / 10
        health_bar = round(move_by * self.current_player.lives)

        pygame.draw.rect(self.win, (255, 0, 0), (1270, 33, lenght, 10), 0)
        pygame.draw.rect(self.win, (0, 255, 0), (1270, 33, health_bar, 10), 0)

        # draw switch players button
        self.switchButton.draw(self.win)

        # draw play/pause button
        self.playPauseButton.draw(self.win)

        # draw start round button
        self.startRoundButton.draw(self.win)

        # draw current players points to spent if there is no way
        if len(self.current_player.enemys) == 0:
            text = self.font.render(str(self.current_player.points), 1, (0, 0, 0))
            self.win.blit(text, (85, 100))

        # draw which player now plays
        if self.current_player == self.player1:
            text = self.font.render("player 1", 1, (0, 0, 0))
        else:
            text = self.font.render("player 2", 1, (0, 0, 0))
        start_x = 100

        self.win.blit(text, (start_x - text.get_width() - 1, 10))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["longRangeTower", "rangeTower", "damageTower"]
        object_list = [LongRangeTower(x, y), DamageTower(x, y), RangeTower(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")


#multi = Multiplayer()
#multi.run()
