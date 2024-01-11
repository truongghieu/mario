import sys

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import object,zombie
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        # set up for pygame
        pygame.init()
        pygame.display.set_caption('Zombie Killer')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.dim = [2,2]
        # Variables
        self.movement = [False, False]
        self.assets = {

            'background': load_image('background.png'),
            'gameplay_base' :load_image('base.png'),
            'cell': load_image('cells/cell_0.png'),
            'clouds': load_images('clouds'),
            'zombie': load_images('zombies'),
            
        }
        
        # Object setup
        self.clouds = Clouds(self.assets['clouds'], count=5)
        self.scroll = [0, 0]
        self.base = object(self.assets['gameplay_base'], (35, 30))
        self.cells = []
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                self.cells.append(object(self.assets['cell'], (32+x*80,30+ y*80)))

        

        
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

            # pygame.draw.rect(self.display, (255, 0, 0), (0, 0, 80,80))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()