import pygame

class object:
    def __init__(self, image, position):
        self.image = image
        self.position = position

    def render(self, display, offset=(0, 0)):
        display.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))   
    
    def update(self):
        pass    


