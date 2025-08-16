# lib
import sys
import pygame
import random
import os

# Config
from CONFIG import *

# System 
from scripts.system.utils import load_image, load_images,Animation
from scripts.system.entities import object
from scripts.system.text import generate_font,show_text
from scripts.system.sound import load_snd,load_kill
from scripts.system.enum import game_state
from scripts.system.tilemap import Tilemap

# Object
from scripts.clouds import Clouds,Cloud
from scripts.button import button
from scripts.effect import effect
from scripts.player import Player 
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
        pygame.init()
        pygame.display.set_caption('Test particles')
        # screen
        self.screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
        self.display = pygame.Surface(DISPLAY_DIMENSIONS)
        self.clock = pygame.time.Clock()
        
        self.data = {
            'logo':load_image('logo.png'),          
            'clouds' : load_images('clouds'),
            'test_particle' : Animation(load_images('particles/smoke_particle'), 5, True)
            }

        #self.clouds = Cloud((0,100) , self.data['clouds'][0],random.random()*2+0.5,0.5)
        self.clouds = Clouds(self.data['clouds'])
        self.particle = particle(self.data['test_particle'],(DISPLAY_DIMENSIONS[0]//2,DISPLAY_DIMENSIONS[1]//2),enabled = True,quantity = 30,speed = 5)
        self.scroll = (0,0)
    def gameplay(self):
        while True:
            self.display.fill((0,0,0))

            # self.display.blit(self.data['logo'], (0, 0))
            
            # Update your object here
            #self.clouds.update()
            self.particle.update()
            #if self.particle.enabled == False:
            #    self.particle.enabled = True
            
            # render your object here
            # self.clouds.render(self.display, offset=self.scroll)
            self.particle.render(self.display, offset=self.scroll)

            # try to update scroll
            # self.scroll = (self.scroll[0] + random.randint(-2,5), self.scroll[1] + random.randint(-2,5))
            #show_text("Tim Adventure",10,2 , 1,185,self.font_2,self.display)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.particle.enabled = not self.particle.enabled
            self.clock.tick(60)
            self.screen.blit(pygame.transform.scale(self.display, SCREEN_DIMENSIONS), (0, 0))
            pygame.display.update()




game = Game()
game.gameplay()
