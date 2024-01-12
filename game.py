import sys
import pygame
import random

from scripts.utils import load_image, load_images,Animation
from scripts.entities import object,zombie
from scripts.clouds import Clouds
from scripts.zombie_manager import zombie_manager

class Game:
    def __init__(self):
        # set up for pygame
        pygame.init()
        pygame.display.set_caption('Zombie Killer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        # Variables
        self.movement = [False, False]
        self.last_mouse_pos = [0, 0]

        self.mouse_timer = 5
        self.current_time_mouse = self.mouse_timer
        
        self.assets = {

            'background': load_image('background.png'),
            'gameplay_base' :load_image('base.png'),
            'cell': load_image('cells/cell_1.png'),
            'clouds': load_images('clouds'),
            'zombie': load_images('zombies'),
        }

        self.zombie_manager_s = zombie_manager(zombie(Animation(self.assets['zombie'], 50,loop=False),[0,0],False), zombie_count=8, zombie_spawn_time=50)
        # self.zombie_manager_s.zombies[2].enable = True
        # Object setup
        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.scroll = [0, 0]
        self.base = object(self.assets['gameplay_base'], (35, 30))
        self.cells = []
        for spawn in self.zombie_manager_s.spawn_positions:
            self.cells.append(object(self.assets['cell'], spawn))


    def run(self):
        while True:

            self.display.blit(self.assets['background'], (0, 0))
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.base.render(self.display, offset=render_scroll)
            self.base.update()

            for cell in self.cells:
                cell.render(self.display, offset=render_scroll)
                cell.update()

            self.zombie_manager_s.update()
            self.zombie_manager_s.render(self.display,offset=render_scroll)  
        
            # pygame.draw.rect(self.display, (255, 0, 0), (0, 0, 80,80))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # get mouse position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.last_mouse_pos = pygame.mouse.get_pos()
                    # self.last_mouse_pos = self.last_mouse_pos / self.display.get_size() * self.screen.get_size()
                    # convert tuble to list
                    self.last_mouse_pos = list(self.last_mouse_pos)
                    # convert to surface position
                    self.last_mouse_pos = [self.last_mouse_pos[0] / self.screen.get_size()[0] * self.display.get_size()[0],self.last_mouse_pos[1] / self.screen.get_size()[1] * self.display.get_size()[1]]
                    
                    for zombie in self.zombie_manager_s.zombies:
                        if zombie.check_mouse_collision(self.last_mouse_pos):
                            print(zombie.position)
                            zombie.enable = False
                            print("collision")
                            break
                if event.type == pygame.MOUSEBUTTONUP:
                    self.last_mouse_pos = [0,0]

                    # check if mouse position is over the button
                # if event.type == pygame.MOUSEBUTTONUP:
                #     self.last_mouse_pos = [0,0]

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    

Game().run()