import pygame
import json 
from scripts.enemy import snake
NEIGHBOR_OFFSETS = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
PHYSICS_TILES = {"base","stone"}
ENEMY_TYPES = {"snake_spawn"}



class Tilemap:
    def __init__(self, game,tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.spawned = False
        self.editor_mode = False

        # for i in range(10):
        #     self.tilemap[str(3+i)+';5'] = {'type':'grass','variant':0,'pos':(3+i,5)}
        #     self.tilemap['10;'+str(2+i)] = {'type':'stone','variant':0,'pos':(10,2+i)}

    def render(self,surface,offset=(0,0)):
        for x in range(offset[0]//self.tile_size,(offset[0]+surface.get_width())//self.tile_size+1):
            for y in range(offset[1]//self.tile_size,(offset[1]+surface.get_height())//self.tile_size+1):
                check_loc = str(x)+';'+str(y)
                if check_loc in self.tilemap:
                    tile = self.tilemap[check_loc]
                    surface.blit(self.game.assets[tile['type']][tile['variant']],(x*self.tile_size - offset[0],y*self.tile_size - offset[1]))
                    
        # for loc in self.tilemap:
        #     tile = self.tilemap[loc]
        #     surface.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0]*self.tile_size - offset[0],tile['pos'][1]*self.tile_size - offset[1]))

        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] - offset[0],tile['pos'][1] - offset[1]))
            if tile['type'] in ENEMY_TYPES and not self.spawned and self.editor_mode == False:
                if tile['type'] == 'snake_spawn':
                    self.game.enemies.append(snake(self.game.assets['snake'],tile['pos']))
        
        self.spawned = True                
        # enemy
            


    def tile_around(self,pos):
        tiles = []
        tile_loc = (int(pos[0]/self.tile_size),int(pos[1]/self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0]+offset[0])+';'+str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self,pos):
        rects = []
        for tile in self.tile_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0]*self.tile_size,tile['pos'][1]*self.tile_size,self.tile_size,self.tile_size))

        return rects
    
    def save_file(self,path):
        f = open(path,'w')
        json.dump({"tilemap":self.tilemap,"tile_size":self.tile_size,"offgrid_tiles":self.offgrid_tiles},f)
        f.close()

    def load_file(self,path):
        f = open(path,'r')
        data = json.load(f)
        self.tilemap = data['tilemap']
        self.tile_size = data['tile_size']
        self.offgrid_tiles = data['offgrid_tiles']
        f.close()