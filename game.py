# lib
import sys
import pygame
import random

# System 
from scripts.system.utils import load_image, load_images,Animation
from scripts.system.entities import object,zombie,hammer
from scripts.system.text import generate_font,show_text
from scripts.system.sound import load_snd,load_kill
from scripts.system.enum import game_state
from scripts.system.tilemap import Tilemap

# Object
from scripts.base import base
from scripts.clouds import Clouds
from scripts.zombie_manager import zombie_manager
from scripts.boss_manager import boss_manager
from scripts.boss.greenskin import greenskin
from scripts.card import card,card_score,card_damage,card_zombie,card_manager
from scripts.button import button
from scripts.effect import effect
from scripts.player import Player 

font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3],'<':[3],'>':[3],';':[1]}

class Game:
    def __init__(self):
        # cc
        # set up for pygame
        pygame.init()
        pygame.display.set_caption('Zombie Killer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.font_1 = generate_font('data/fonts/small_font.png',font_dat,5,8,(185,57,57))
        self.font_2 = generate_font('data/fonts/small_font.png',font_dat,5,8,(51,34,40))
        # Variables
        # music 
        pygame.mixer.music.load('data/main.wav')
        self.hit_clip = load_snd('explosion')
        # ---------------
        self.last_mouse_pos = [0, 0]
        self.timer = 0
        self.score = 0
        self.kill_clip = []
        self.time_effect_active_boss = 0 
        for i in range(2,19):
            self.kill_clip.append(load_kill(str(i)))
        self.assets = {
            'logo': load_image('logo.png'),
            'background': load_image('background.png'),
            'start_button': load_image('button/start.png'),
            'score_window' : load_image('score_window.png'),
            'clouds': load_images('clouds'),
            'decor' : load_images('tiles/decor'),
            'stone' : load_images('tiles/stone'),
            'grass' : load_images('tiles/grass'),
            'player_idle' : Animation(load_images('entities/boss_0'),10,True),
            'hit_effect' : Animation(load_images('particles/boom'),3,False),
            # Card
            'card_score' : load_image('cards/card_health.png'),
            'card_damage' : load_image('cards/card_damage.png'),
            'card_zombie' : load_image('cards/card_zombie.png'),
        }
        self.tilemap = Tilemap(self,tile_size=16)
        self.game_state = game_state.menu
        self.game_logo = object(self.assets['logo'], (self.display.get_size()[0] / 2 - self.assets['logo'].get_width() / 2, 50))
        self.start_button = button(self.assets['start_button'], (self.display.get_size()[0] / 2 - self.assets['start_button'].get_width() / 2, 120), True)
        
        
        
        
        self.player = Player(self.assets['player_idle'],[100,100])
        # card and card manager
        # self.card_score = card_score(self.assets['card_score'],(100,250),self)
        # self.card_damage = card_damage(self.assets['card_damage'],(100,250),self)
        # self.card_zombie = card_zombie(self.assets['card_zombie'],(100,250),self)
        # self.card_manager = card_manager(self.display)
        # self.card_manager.add_card(self.card_score)
        # self.card_manager.add_card(self.card_damage)
        # self.card_manager.add_card(self.card_zombie)

   

        # Decorations
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.scroll = [0, 0]
        self.score_window = object(self.assets['score_window'], (0, 0))
        self.movement = [0,0]

    def gameplay(self):
        # pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.3)
        # self.hit_clip.set_volume(0.1)
        # self.boss_manaer_s.enable = True
        # self.boss_manaer_s.wake_up_boss(0)

        while self.game_state == game_state.gameplay:
            if self.score < 0:
                self.game_state = game_state.menu
                self.menu()
                break
            self.timer += 1



            self.display.blit(self.assets['background'], (0, 0))
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            self.tilemap.render(self.display)

            self.player.update([self.movement[1] - self.movement[0],0])
            self.player.render(self.display,offset=render_scroll)

            # show_text("Score : "+str(self.score) ,10,10 , 1,185,self.font_2,self.display)


    

            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.K_DOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = 1



            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    def menu(self):
        self.score = 0
        self.timer = 0

        while self.game_state == game_state.menu:
            self.display.blit(self.assets['background'], (0, 0))
            self.clouds.update()
            self.clouds.render(self.display, offset=(0, 0))
            self.game_logo.render(self.display, offset=(0, 0))
            self.game_logo.update()
            self.start_button.render(self.display, offset=(0, 0))
            self.start_button.update()
            show_text("Zombie Killer",10,10 , 1,185,self.font_1,self.display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouserealpos = pygame.mouse.get_pos()
                    pos_convert = (mouserealpos[0]*self.display.get_size()[0]/self.screen.get_size()[0],mouserealpos[1]*self.display.get_size()[1]/self.screen.get_size()[1])
                    if self.start_button.check_mouse_collision(pos_convert):
                        self.game_state = game_state.gameplay
                        self.gameplay()
             
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    def change_state(self,state):
        self.game_state = state

game = Game()
game.menu()