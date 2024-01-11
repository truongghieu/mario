import sys

import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import object
from scripts.clouds import Clouds

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
        self.assets = {

            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'zombie': load_images('zombies'),
            'gameplay_base' :load_image('base.png'),
        }
        
        # Object setup
        self.clouds = Clouds(self.assets['clouds'], count=5)
        self.scroll = [0, 0]
        self.base = object(self.assets['gameplay_base'], (35, 30), scale=1)

        
    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.base.render(self.display, offset=render_scroll)
            self.base.update()

        
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()