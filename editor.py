# lib
import sys
import pygame
import random

# System 
from scripts.system.utils import load_image, load_images,Animation
from scripts.system.text import generate_font,show_text
from scripts.system.sound import load_snd,load_kill
from scripts.system.enum import game_state
from scripts.system.tilemap import Tilemap

# Object
from scripts.button import button
from scripts.player import Player 

RENDER_SCALE = 5.0
class Editor:
    def __init__(self):
        # cc
        # set up for pygame
        pygame.init()
        pygame.display.set_caption('Editor')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((128, 96))
        self.clock = pygame.time.Clock()

        # Variables
        # music 
        pygame.mixer.music.load('data/main.wav')
        self.hit_clip = load_snd('explosion')
        # ---------------


        self.assets = {
            # object map
 
            'base' : load_images('tiles/grass'),
            'decor' : load_images('tiles/decor'),
            'tree' : load_images('tiles/tree'),

            # spawning place
            'snake_spawn': load_images('entities/snake'),
            # player

            # BONUS ITEM
            
            'player_upgrade_point' : load_images('item/player_upgrade_point'),
            'bullet_upgrade_point' : load_images('item/bullet_upgrade_point'),
            'gold' : load_images('item/gold'),
            'next_level' : load_images('next_level'),
        
        }
        self.enemies = []
        self.tilemap = Tilemap(self,tile_size=8)
        self.tilemap.editor_mode = True
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        # self.player.velocity = [0,2]
        # card and card manager
        # self.card_score = card_score(self.assets['card_score'],(100,250),self)
        # self.card_damage = card_damage(self.assets['card_damage'],(100,250),self)
        # self.card_zombie = card_zombie(self.assets['card_zombie'],(100,250),self)
        # self.card_manager = card_manager(self.display)
        # self.card_manager.add_card(self.card_score)
        # self.card_manager.add_card(self.card_damage)
        # self.card_manager.add_card(self.card_zombie)

        self.map_file = "map/level_2.json"

        # Decorations
        self.scroll = [0, 0]
        self.movement = [False, False, False, False]
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        try:
            self.tilemap.load_file(self.map_file)
        except FileNotFoundError:
            pass
    def gameplay(self):
        # pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.3)
        # self.hit_clip.set_volume(0.1)
        # self.boss_manaer_s.enable = True
        # self.boss_manaer_s.wake_up_boss(0)

        while self.game_state == game_state.gameplay:
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))
            
            

            current_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile.set_alpha(150)
            # print(self.tilemap.physics_rects_around(self.player.position))
            self.display.fill((0, 0, 0))
            self.display.blit(current_tile,(1 ,1))
            self.tilemap.render(self.display, offset=render_scroll)


            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0]//RENDER_SCALE,mpos[1]//RENDER_SCALE)
            tile_pos = (int(mpos[0]+self.scroll[0])//self.tilemap.tile_size,int(mpos[1]+self.scroll[1])//self.tilemap.tile_size)
            
            if self.ongrid:
                self.display.blit(current_tile,(tile_pos[0]*self.tilemap.tile_size - render_scroll[0],tile_pos[1]*self.tilemap.tile_size - render_scroll[1]))
            else:
                self.display.blit(current_tile,(mpos[0] ,mpos[1] ))


            if self.clicking and self.ongrid:
                # print(str(tile_pos[0])+';'+str(tile_pos[1]))
                self.tilemap.tilemap[str(tile_pos[0])+';'+str(tile_pos[1])] = {'type':self.tile_list[self.tile_group],'variant':self.tile_variant,'pos':tile_pos}
            if self.right_clicking :
                if str(tile_pos[0])+';'+str(tile_pos[1]) in self.tilemap.tilemap:
                    del self.tilemap.tilemap[str(tile_pos[0])+';'+str(tile_pos[1])]
                offgrid = self.tilemap.offgrid_tiles
                for tile in offgrid:
                    tile_image = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - render_scroll[0],tile['pos'][1] - render_scroll[1],self.tilemap.tile_size,self.tilemap.tile_size)
                    if tile_rect.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
                        
            if self.movement == [0,0]:
                self.player.image = self.assets['player_idle_right']
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type':self.tile_list[self.tile_group],'variant':self.tile_variant,'pos':(mpos[0] + render_scroll[0],mpos[1] + render_scroll[1])})
                        print(len(self.tilemap.offgrid_tiles))
                    if event.button == 3:
                        self.right_clicking = True
                    if not self.shift:
                        if event.button == 4:
                            self.tile_variant = 0
                            if len(self.assets[self.tile_list[self.tile_group]]) > 1:
                                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        if event.button == 5:
                            self.tile_variant = 0
                            if len(self.assets[self.tile_list[self.tile_group]]) > 1:
                                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                    else:
                        if event.button == 4:
                            if len(self.assets[self.tile_list[self.tile_group]]) > 1:
                                self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            if len(self.assets[self.tile_list[self.tile_group]]) > 1:
                                self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_SPACE:
                        self.tilemap.save_file(self.map_file)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                



            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
   
game = Editor()
game.game_state = game_state.gameplay
game.gameplay()