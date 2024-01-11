import pygame
class object:
    def __init__(self, image, position, scale=1):
        self.image = image
        self.position = position
        self.scale = scale

    def render(self, display, offset=(0, 0)):
        display.blit(pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale))), (self.position[0] - offset[0], self.position[1] - offset[1]))   
    
    def update(self):
        pass    

class zombie(object):
    def __init__(self, image, position, scale=1,timer = 1):
        super().__init__(image, position, scale)
        
        