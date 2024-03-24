# lib
import sys
import pygame
import random
import os


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
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((128, 96))
        self.clock = pygame.time.Clock()
        self.font_1 = generate_font('data/fonts/small_font.png',font_dat,5,8,(185,57,57))
        self.font_2 = generate_font('data/fonts/small_font.png',font_dat,5,8,(51,34,40))
        # Variables
        # ______________SOUND___________________
        pygame.mixer.music.load('data/music.wav')
        self.hit_clip = load_snd('hit')
        self.jump_clip = load_snd('jump')
        self.collect_clip = load_snd('pickupCoin')
        self.music_volume = 0.3
        self.sfx_volume = 0.3
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
            'options_button': load_image('button/option.png'),
            'about_button': load_image('button/about.png'),
            'exit_button': load_image('button/exit.png'),
            'panel' : load_image('panel.png'),
            'about_panel' : load_image('about.png'),
            'heart': load_image('ui/heart.png'),
            'clouds': load_images('clouds'),

            'base' : load_images('tiles/grass'),
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

        # ----------------- GAMEPLAY -----------------
        self.game_level = 0
        self.tilemap = Tilemap(self)
        self.game_state = game_state.menu
        # self.game_logo = object(self.assets['logo'], (self.display.get_size()[0] / 2 - self.assets['logo'].get_width() / 2, 2))
        # components in UI 
       
        self.bullet_list = []
        # create 100 bullets
        for i in range(100):
            self.bullet_list.append(bullet(self.assets["bullet"],[-100,-100],[3,0],False))
        
        
        self.player = Player(self,self.assets['player_run_right'],[50,50],8)


        # __________________ UI __________________
        self.coint_img = object(self.assets['gold'][0],(2,2))
        self.heart_img = object(self.assets['heart'],(30,3))
        self.start_button = button(self.assets['start_button'], (self.display.get_size()[0] / 2 - self.assets['start_button'].get_width() / 2 - 30, 10), True)
        self.options_button = button(self.assets['options_button'], (self.display.get_size()[0] / 2 - self.assets['options_button'].get_width() / 2 - 30, 30), True)
        self.about_button = button(self.assets['about_button'], (self.display.get_size()[0] / 2 - self.assets['about_button'].get_width() / 2 - 30, 50), True)
        self.exit_button = button(self.assets['exit_button'], (self.display.get_size()[0] / 2 - self.assets['exit_button'].get_width() / 2 - 30, 70), True)
        self.option_panel = option(self.assets['panel'], (0, 0),handle=self)
        self.about_panel = about(self.assets['about_panel'], (0, 0))
        # ----------------- DECORATION -----------------
        self.clouds = Clouds(self.assets['clouds'], count=8)
        self.scroll = [0, 0]
        self.movement = [0,0]
        # ----------------- PARTICLE EFFECTS --------------
        self.hit_effect = particle(self.assets["bullet_particle"],[0,0],10,False)
        self.running_effect = running_effect(self.assets["running_effect"],[0,0],10,False)
        
        
        # ------------------ LIST GAME OBJECT -------------------
        self.enemies = []
        self.collectible_items = []

    def gameplay(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.music_volume)
        self.hit_clip.set_volume(self.sfx_volume)
        self.collect_clip.set_volume(self.sfx_volume)
        self.jump_clip.set_volume(self.sfx_volume)
        # self.boss_manaer_s.enable = True
        # self.boss_manaer_s.wake_up_boss(0)
        self.tilemap.load_file('map/level_'+str(self.game_level)+'.json')

        while self.game_state == game_state.gameplay:
            if self.player.player_health <= 0:
                self.game_state = game_state.menu
                self.menu()
                break
            self.timer += 1
            if self.player.position[1] > 500:
                self.player.player_health -= 1
                self.player.reset()
            
            
            
            # print(self.tilemap.physics_rects_around(self.player.position))
            self.scroll[0] += (self.player.rect().centerx - self.display.get_size()[0] / 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_size()[1] / 2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))


            self.display.blit(self.assets['background'], (0, 0))
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update([self.movement[1] - self.movement[0],0],self.tilemap)
            self.player.render(self.display,offset=render_scroll)
            
            # EFFECTS
            if self.player.running:
                if self.player.flip:
                    self.running_effect.position = [self.player.position[0] + 4,self.player.position[1] +4]
                else:
                    self.running_effect.position = [self.player.position[0] - 4,self.player.position[1] +4]
                self.running_effect.enabled = True
            else:
                self.running_effect.enabled = False
            self.hit_effect.update()
            self.hit_effect.render(self.display,offset=render_scroll)
            self.running_effect.update()
            self.running_effect.render(self.display,offset=render_scroll)
            # processing bullets
            if self.player.shooting:
                for bullet in self.bullet_list:
                    if not bullet.enabled:
                        bullet.position = self.player.shoot_pos
                        if self.player.flip:
                            bullet.dir = True
                            self.player.velocity[0] = 1
                        elif self.player.flip == False:
                            bullet.dir = False
                            self.player.velocity[0] = -1
                        bullet.enabled = True
                        break
            else:
                self.player.velocity[0] = 0



            for bullet in self.bullet_list:
                bullet.update(self.player.position)
                bullet.render(self.display,offset=render_scroll)
        
            # LIST GAME OBJECT UBDATE
            for enemy in self.enemies:
                enemy.update(self.tilemap)
                enemy.render(self.display,offset=render_scroll)
                if enemy.rect().colliderect(self.player.rect()):
                    self.player.player_health -= 1
                    self.player.reset()
                for bullet in self.bullet_list:
                    if bullet.enabled:
                        if bullet.rect().colliderect(enemy.rect()):
                            bullet.enabled = False
                            self.enemies.remove(enemy)
                            self.hit_effect.position = enemy.position
                            self.hit_effect.enabled = True
                            self.hit_clip.play()
                            break
            for item in self.collectible_items:
                if item.update(self.player.rect()):
                    self.collect_clip.play()
                    if item.type == "next_level":
                        self.next_level()
                    if item.type == "gold":
                        self.score += 1
                    if item.type == "bullet_upgrade":
                        for b in self.bullet_list:
                            b.upgrade()
                    if item.type == "player_upgrade":
                        self.player.upgrade()
                    self.collectible_items.remove(item)
                    
                item.render(self.display,offset=render_scroll)

            self.coint_img.render(self.display)
            self.heart_img.render(self.display)
            show_text(str(self.score),13,3,1,185,self.font_2,self.display)
            show_text('x'+str(self.player.player_health),38,3,1,185,self.font_2,self.display)
            
            if self.player.player_health <= 0:
                self.game_state = game_state.menu
                self.menu()
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.image = self.assets['player_run_left']
                        self.player.running = True
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.player.image = self.assets['player_run_right']
                        self.movement[1] = True
                        self.player.running = True
                        
                    
                    if event.key == pygame.K_UP:
                        self.player.jump()
                        self.jump_clip.play()
                    
                    if event.key == pygame.K_SPACE:
                        self.player.auto_shoot = True 
                  
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                        self.player.running = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                        self.player.running = False
                    if event.key == pygame.K_SPACE:
                        self.player.auto_shoot = False
                



            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)
    def menu(self):
        self.score = 0
        self.timer = 0
        self.player.reset()
        self.score = 0
        self.game_level = 0
        self.player.player_health = 3
        self.movement = [0,0]
        self.collectible_items = []
        self.enemies = []
        while self.game_state == game_state.menu:
            self.display.blit(self.assets['background'], (0, 0))
            self.clouds.update()
            self.clouds.render(self.display, offset=(0, 0))
            # self.game_logo.render(self.display, offset=(0, 0))
            # self.game_logo.update()
            self.start_button.render(self.display, offset=(0, 0))
            self.start_button.update()
            self.options_button.render(self.display, offset=(0, 0))
            self.options_button.update()
            self.about_button.render(self.display, offset=(0, 0))
            self.about_button.update()
            self.exit_button.render(self.display, offset=(0, 0))
            self.exit_button.update()
            self.option_panel.render(self.display, offset=(0, 0))
            self.option_panel.update()
            self.about_panel.render(self.display, offset=(0, 0))
            self.about_panel.update()
            show_text("Tim Adventure",10,2 , 1,185,self.font_2,self.display)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouserealpos = pygame.mouse.get_pos()
                    pos_convert = (mouserealpos[0]*self.display.get_size()[0]/self.screen.get_size()[0],mouserealpos[1]*self.display.get_size()[1]/self.screen.get_size()[1])
                    if self.start_button.check_mouse_collision(pos_convert):
                        self.game_state = game_state.gameplay
                        self.gameplay()
                    if self.exit_button.check_mouse_collision(pos_convert):
                        pygame.quit()
                        sys.exit()
                    if self.options_button.check_mouse_collision(pos_convert):
                        self.option_panel.enabled = not self.option_panel.enabled
                    if self.about_button.check_mouse_collision(pos_convert):
                        self.about_panel.enabled = not self.about_panel.enabled
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    def change_state(self,state):
        self.game_state = state

    def next_level(self):
        if self.game_level < len(os.listdir('map')) - 1:
            self.game_level += 1
        self.tilemap.load_file('map/level_'+str(self.game_level)+'.json')
        self.player.reset()
        for bullet in self.bullet_list:
            bullet.reset()
        self.game_state = game_state.gameplay
        self.gameplay()
    

game = Game()
game.game_state = game_state.menu
game.menu()