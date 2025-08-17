# lib
import sys
import pygame
import random
import os
from CONFIG import *

# System 
from scripts.system.utils import load_image, load_images,Animation
from scripts.system.entities import object
from scripts.system.text import generate_font,show_text
from scripts.system.sound import load_snd,load_kill
from scripts.system.enum import game_state
from scripts.system.tilemap import Tilemap

# Object
from scripts.clouds import Clouds
from scripts.button import button
from scripts.effect import effect
from scripts.player import Player 
from scripts.player_topdown import topdown_player
from scripts.bullet import bullet
from scripts.upgrade_bonus import collectable_object_bullet_upgrade,collectable_object_player_upgrade


from scripts.panel import panel,option,about
# Enemy
from scripts.particle import particle,running_effect

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
        pygame.display.set_caption('TIM Adventure')
        self.screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
        self.display = pygame.Surface(DISPLAY_DIMENSIONS)
        self.clock = pygame.time.Clock()
        self.font_1 = generate_font('data/fonts/small_font.png',font_dat,5,8,(185,57,57))
        self.font_2 = generate_font('data/fonts/small_font.png',font_dat,5,8,(51,34,40))
        # Variables
        # ______________SOUND___________________
        self.last_mouse_pos = [0, 0]
        self.timer = 0
        self.score = 0
        self.kill_clip = []
        self.time_effect_active_boss = 0 
        self.scroll = [0, 0]
        self.movement = [0, 0]
        for i in range(2,19):
            self.kill_clip.append(load_kill(str(i)))
        self.assets = {
            'logo': load_image('logo.png'),
            'background': load_image('background.png'),
            'start_button': load_image('button/start.png'),
            'options_button': load_image('button/option.png'),
            'about_button': load_image('button/about.png'),
            'exit_button': load_image('button/exit.png'),
            'panel' : load_image('panel.png'),
            'about_panel' : load_image('about.png'),
            'heart': load_image('ui/heart.png'),
            'clouds': load_images('clouds'),

            'grass' : load_images('tiles/grass'),
            'decor' : load_images('tiles/decor'),
            'tree' : load_images('tiles/tree'),
            'snake_spawn' : load_images('entities/snake_spawn'),
            # PLAYER ANIMATIONS
            'player_idle_right' : Animation(load_images('player/idle_right'),10,True),
            'player_idle_left' : Animation(load_images('player/idle_left'),10,True),
            'player_run_right' : Animation(load_images('player/run_right'),10,True),
            'player_run_left' : Animation(load_images('player/run_left'),10,True),
            'player_jump_right' : Animation(load_images('player/jump_right'),13,True),
            'player_jump_left' : Animation(load_images('player/jump_left'),13,True),
            'hit_effect' : Animation(load_images('particles/boom'),3,False),
            'bullet' : load_image('bullet.png'),
            # PARTICLES
            'bullet_particle' : Animation(load_images('particles/particle'),10,False),
            'running_effect' : Animation(load_images('particles/smoke_particle'),5,False),
     
            # ENEMIES
            'snake' : Animation(load_images('entities/snake'),10,True),
            'snake_spawn' : load_images('entities/snake'),
    
            # BONUS ITEM
            
            'player_upgrade_point' : load_images('item/player_upgrade_point'),
            'bullet_upgrade_point' : load_images('item/bullet_upgrade_point'),
            'gold' : load_images('item/gold'),
            # NEXT LEVEL POINT
            'next_level' : load_images('next_level')

        }

        
        self.tilemap = Tilemap(self)
        self.clouds = Clouds(self.assets['clouds'], count=8)
        self.player = topdown_player(self.assets['player_idle_right'],( (DISPLAY_DIMENSIONS[0]//2), (DISPLAY_DIMENSIONS[1]//2)))

    def gameplay(self):
        # this is for starting setup for gameplay
        while True:
            #print(self.scroll)
            self.display.blit(pygame.transform.scale(self.assets['background'], DISPLAY_DIMENSIONS), (0, 0))
            # ----------------- GAMEPLAY -----------------
            self.clouds.update()
            # ----------------- UPDATE Part -----------------
            # Update this for player scroll will depend on player posistion
            render_scroll = self.scroll
            self.player.update()
            # ----------------- RENDER Part -----------------
            self.tilemap.render(self.display,offset=(0,0))
            self.clouds.render(self.display, offset=render_scroll)
            self.player.render(self.display, offset=render_scroll)
            # self.game_logo = object(self.assets['logo'], (self.display.get_size()[0] / 2 - self.assets['logo'].get_width() / 2, 2))
            # components in UI  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # ESC
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                # MOVEMENT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        self.scroll[0] += 5
                    if event.key == pygame.K_RIGHT:
                        #self.player.image = self.assets['player_run_right']
                        self.movement[1] = True
                        #self.player.running = True
                        self.scroll[0] -= 5

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.gameplay()

